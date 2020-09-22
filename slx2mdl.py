#!/usr/bin/python3

import glob
from commons import *
from tags_model import *
from transform_stateflow import stateflow_xml2mdl
import time


class Transformer:
    # controls whether to preetify the output mdl
    # This can be overridden from Transformer.initialize()
    _preetify = False

    filepath_slx = None  # input
    filepath_mdl = None  # output
    filepath_original_mdl = None
    filepath_original_mdl_preetified = None
    dirpath_working = None
    dirpath_batch_prod_output = None  # see docstring of Transformer.initialize()
    dirpath_slx_extracted = None
    filepath_merged_commented = None
    filepath_merged_uncommented = None

    filepath_stateflow = None
    filepath_stateflow_preprocessed = None

    filepath_output_model_only_unpreetified = None
    filepath_output_model_only_preetified = None
    filepath_output_stateflow_only = None

    filepath_merged_commented_no_multiline_str_content = None
    filepath_merged_uncommented_no_multiline_str_content = None
    filepath_mdl_unpreetified = None
    filepath_mdl_preetified = None

    filepath_original_mdl_at_working_directory = None
    filepath_original_mdl_at_current_directory = None
    filepath_output_mdl_at_current_directory = None

    filepath_error_log = None

    @classmethod
    def _extract_slx_archive(cls):
        """Extract slx archive (located in cls.filepath_slx).
        The extracted files will be in cls.dirpath_slx_extracted"""
        with zipfile.ZipFile(cls.filepath_slx, 'r') as zip_ref:
            zip_ref.extractall(cls.dirpath_slx_extracted)

    @classmethod
    def _merge_xmls(cls, output_filepath):
        """Merge xml files in the slx archive into one big xml file
        Some xml files (eg. stateflow.xml) won't be merged.
        """

        # files are in the order in which the corresponding information appears in the final mdl file
        # while this is not a requirement, it will keep the information look more 'organized' to a human reader.
        files = [
            'simulink/blockdiagram.xml',
            'simulink/windowsInfo.xml',
            # 'slx-files/metadata/coreProperties.xml',

            # plugins
            'simulink/plugins/AnimationPlugin',  # first found in sldemo_suspn ;
            'simulink/plugins/DiagnosticSuppressor.xml',
            'simulink/plugins/LogicAnalyzerPlugin.xml',
            'simulink/plugins/NotesPlugin.xml',
            'simulink/plugins/SLCCPlugin.xml',
            'simulink/plugins/WebScopes_FoundationPlugin.xml',

            'simulink/configSet0.xml',
            'simulink/bddefaults.xml',
            # 'simulink/configSetInfo.xml',
            'simulink/graphicalInterface.xml',
        ]
        with open(output_filepath, 'w') as wfile:
            for f in files:
                # it is not guarranted that every slx files contains all of these xml files
                # so we proceed only if the file exists.
                p = os.path.join(cls.dirpath_working, 'slx-files', f)
                if os.path.exists(p):
                    with open(p) as rfile:
                        wfile.write('\n\n')
                        comment = f'<!--{f[9:]}-->'  # filename inside comment

                        rfile.readline()  # skip first line
                        for line in rfile:

                            if p.endswith('blockdiagram.xml'):  # file-specific processing
                                # skip <ModelInformation...> and its closing tag (of blockdiagram.xml)
                                if 'ModelInformation' in line:
                                    continue
                                # don't write the last line yet.
                                if line.strip() == '</Model>':
                                    roottag = 'Model'
                                    continue
                                if line.strip() == '</Library>':
                                    roottag = 'Library'
                                    continue
                                if line.strip() == '</Subsystem>':  # first found in simulink/ex_modeling_mechanical_system
                                    roottag = 'Subsystem'
                                    continue

                            line = line[:-1] + comment + '\n'
                            # IMPORTANT: NEVER ADD ANY INDENTATION I.E. NEVER ADD ANY EXTRA SPACES TO THE
                            # LEFT OF THE LINES WHEN WRITING THEM TO THE FILE. OTHERWISE, WE WILL END UP
                            # WITH INVALID STRINGS (FOR MULTILINE STRING CONTENTS). THIS BECOMES FATAL
                            # SOMETIMES -- FOR EXAMPLE: THIS CAN CAUSE INVLID PATH REFERENCES TO LIBRARY
                            # ELEMENTS AND HENCE CORRUPT THE MODEL.
                            wfile.write(line)

            # finally write the closing tag for <Model> or <Library> or <Subsystem>
            wfile.write(f'</{roottag}>')

    @classmethod
    def initialize(cls, args, filepath_slx, dirpath_working, dirpath_batch_prod_output, filepath_mdl=None, preetify=False):
        """Initialize the transformer.

        Parameters: 
        args(dict)          : arguments provided by user 
        filepath_slx(str)   : absolute/relative filepath of input slx file. This is available in args only in 'single' mode, 
                              so we need to pass it. 
        dirpath_working(str): directory where intermediate (and output) files will be produced. 
                              In production mode, this directory will be removed after transformation completes.
        dirpath_batch_prod_output(str) : If 'mode' is 'batch', and 'devt-mode' is 'no', then this directory will contain
                              all output mdl files immediately within itself (i.e. without nesting). If 'devt-mode' is 'yes',
                              this directory won't be created at all.
        filepath_mdl(str)   : absolute/relative filepath of output mdl file 
        preetify(bool)      : If true, output mdl file is preetified. 
        """
        cls._args = args
        cls._preetify = preetify

        # this is needed because Utils is SINGLETON
        Utils.clear_ids()
        UtilsStfl.clear_ids()

        # define all necessary file and directory paths
        # we will always use absolute paths
        cls.filepath_slx = os.path.abspath(filepath_slx)
        cls.dirpath_working = os.path.abspath(dirpath_working)
        cls.dirpath_batch_prod_output = os.path.abspath(dirpath_batch_prod_output) if dirpath_batch_prod_output else None

        if filepath_mdl is None:
            # by default, the output mdl filename will be same as the input slx file with a different extension i.e mdl instead of slx.
            # And the output mdl file will be placed in user's current dirrectory (rather than input slx file's directory.)
            dirpath, filename_without_ext, ext_with_dot = Utils.split_filepath(cls.filepath_slx)
            filepath_mdl = f"{filename_without_ext}.mdl"  # relative wrt current directory

        cls.filepath_mdl = os.path.abspath(filepath_mdl)

        # the path is set irrespective of whether the file exists or not
        cls.filepath_original_mdl = os.path.splitext(cls.filepath_slx)[0] + '_org.mdl'
        cls.filepath_original_mdl_preetified = os.path.join(cls.dirpath_working, 'original_preetified.mdl')

        cls.dirpath_slx_extracted = os.path.abspath(os.path.join(cls.dirpath_working, 'slx-files'))
        cls.filepath_merged_commented = os.path.abspath(os.path.join(cls.dirpath_working, 'merged_commented.xml'))
        cls.filepath_merged_uncommented = os.path.abspath(os.path.join(cls.dirpath_working, 'merged_uncommented.xml'))
        cls.filepath_merged_commented_no_multiline_str_content = os.path.abspath(os.path.join(cls.dirpath_working, 'merged_commented_no_multiline_str_content.xml'))
        cls.filepath_merged_uncommented_no_multiline_str_content = os.path.abspath(os.path.join(cls.dirpath_working, 'merged_uncommented_no_multiline_str_content.xml'))

        cls.filepath_output_model_only_unpreetified = os.path.abspath(os.path.join(cls.dirpath_working, 'output_model_only_unpreetified.mdl'))
        cls.filepath_output_model_only_preetified = os.path.abspath(os.path.join(cls.dirpath_working, 'output_model_only_preetified.mdl'))

        cls.filepath_output_stateflow_only = os.path.abspath(os.path.join(cls.dirpath_working, 'output_stateflow_only.mdl'))

        cls.filepath_mdl_unpreetified = os.path.abspath(os.path.join(cls.dirpath_working, 'output.mdl'))
        cls.filepath_mdl_preetified = os.path.abspath(os.path.join(cls.dirpath_working, 'output_preetified.mdl'))

        cls.filepath_stateflow = os.path.abspath(os.path.join(cls.dirpath_working, 'slx-files', 'simulink', 'stateflow.xml'))
        cls.filepath_stateflow_preprocessed = os.path.abspath(os.path.join(cls.dirpath_working, 'stateflow-preprocessed.xml'))

        cls.filepath_output_mdl_at_current_directory = os.path.abspath('output.mdl')

        # the path is set irrespective of whether the original mdl file exists or not
        cls.filepath_original_mdl_at_working_directory = os.path.abspath(os.path.join(cls.dirpath_working, 'original.mdl'))
        cls.filepath_original_mdl_at_current_directory = os.path.abspath('original.mdl')

        cls.filepath_error_log = os.path.abspath('error-log.txt')

        mode = f"{cls._args['mode']}, {'development' if cls._args['devt_mode'] else 'production'}"

        print(f"\nmode                            : {mode}")
        print(f"filepath_slx                    : {cls.filepath_slx}")
        print(f"filepath_mdl                    : {cls.filepath_mdl}")
        if cls._args['devt_mode']:
            print(f"filepath_original_mdl, if any   : {cls.filepath_original_mdl}")
            print(f"dirpath_working                 : {cls.dirpath_working}")
        if dirpath_batch_prod_output:
            print(f"dirpath_batch_prod_output       : {cls.dirpath_batch_prod_output}")
        print(f"filepath_error_log              : {cls.filepath_error_log}\n")

        # remove previous files and  create all necessary files/folders
        # IMPORTANT: dirpath_batch_prod_output must not be removed or created from here,
        # because doing so would erase output mdl files of pervious models in the same batch.
        # Removing previous dirpath_batch_prod_output (if any), and recreating one
        # is handled by main() method of this module.

        Utils.remove_file(cls.filepath_original_mdl_at_current_directory)
        Utils.remove_file(cls.filepath_output_mdl_at_current_directory)
        Utils.remove_file(cls.filepath_mdl)
        Utils.remove_file('original.slx')  # this file exists if previous transformation was run in 'devt' mode
        Utils.remove_dirpath(cls.dirpath_working)
        Utils.create_dirpath(cls.dirpath_working)
        Utils.create_file(cls.filepath_mdl)

        # copy original mdl file to working directory and current directory
        # do this in this method rather than in transform() so that even if transformation fails,
        # we can still inspect the original mdl file at the working directory and current directory
        if os.path.exists(cls.filepath_original_mdl) and cls._args['devt_mode']:
            Utils.copy_file(cls.filepath_original_mdl, cls.filepath_original_mdl_at_working_directory)
            Utils.copy_file(cls.filepath_original_mdl, cls.filepath_original_mdl_at_current_directory)
            if cls._preetify:
                Utils.preetify_mdl_file(cls.filepath_original_mdl, cls.filepath_original_mdl_preetified)

    @classmethod
    def _preprocess_stateflow(cls, input_filepath, output_filepath):
        with open(cls.filepath_stateflow) as rfile:
            rfile.readline()  # skip first line
            with open(output_filepath, 'w') as wfile:  # intermediate output in output_filepath
                for line in rfile:
                    wfile.write(line)
        Utils.str_contents_multiline_to_singleline(input_filepath=output_filepath, output_filepath=output_filepath)  # write in same file

    @classmethod
    def _remove_intermediate_files_and_dirs(cls):
        """Remove (all) intermediate files produced during the transformation.
        Which files/dirs to remove is decided based on args.

        Parameters: 
        args(dict): arguments passed by user
        """

        # we don't want to remove any intermediate file in 'development' mode.
        if not cls._args['devt_mode']:
            Utils.remove_file(cls.filepath_original_mdl_at_current_directory)
            Utils.remove_file(cls.filepath_output_mdl_at_current_directory)
            Utils.remove_dirpath(cls.dirpath_working)

    @classmethod
    def transform(cls):
        """Transform the slx file at cls.filepath_slx to mdl file
        and save it in cls.filepath_mdl."""

        cls._extract_slx_archive()
        cls._merge_xmls(output_filepath=cls.filepath_merged_commented)

        Utils.uncomment_xml_file(input_filepath=cls.filepath_merged_commented, output_filepath=cls.filepath_merged_uncommented)
        Utils.str_contents_multiline_to_singleline(input_filepath=cls.filepath_merged_commented, output_filepath=cls.filepath_merged_commented_no_multiline_str_content)
        Utils.str_contents_multiline_to_singleline(input_filepath=cls.filepath_merged_uncommented, output_filepath=cls.filepath_merged_uncommented_no_multiline_str_content)

        # transform Model
        with open(cls.filepath_merged_uncommented_no_multiline_str_content) as file:
            xml = file.read()
        xml = xml.strip()
        modelOrLibraryOrSubsystem = ModelOrLibraryOrSubsystem(xml, parent_xml=None)
        mdl = modelOrLibraryOrSubsystem.strmdl
        with open(cls.filepath_output_model_only_unpreetified, 'w') as file:
            file.write(mdl)

        Utils.copy_file(cls.filepath_output_model_only_unpreetified, cls.filepath_mdl_unpreetified)

        if cls._preetify:
            Utils.preetify_mdl_file(cls.filepath_output_model_only_unpreetified, cls.filepath_output_model_only_preetified)
            Utils.copy_file(cls.filepath_output_model_only_preetified, cls.filepath_mdl_preetified)

        # handle stateflow
        if os.path.exists(cls.filepath_stateflow):
            # transform Statelfow
            cls._preprocess_stateflow(input_filepath=cls.filepath_stateflow, output_filepath=cls.filepath_stateflow_preprocessed)
            with open(cls.filepath_stateflow_preprocessed) as file:
                stfl_xml = file.read()
                stfl_mdl = stateflow_xml2mdl(stfl_xml)  # stateflow transformation
            with open(cls.filepath_output_stateflow_only, 'w') as file:
                file.write(stfl_mdl)

            # Append stateflow content to both unpreetified as well as preetified versions of mdl file
            with open(cls.filepath_mdl_unpreetified, 'a') as file:
                file.write(stfl_mdl)
            if cls._preetify:
                with open(cls.filepath_mdl_preetified, 'a') as file:
                    file.write(stfl_mdl)

        # copy file
        # preetifying output may introduce error in the mdl file,
        # so the unpreetified version is copied as the output to filepath_mdl
        Utils.copy_file(cls.filepath_mdl_unpreetified, cls.filepath_mdl, ignore_same_file_error=True)

        if cls._args['devt_mode']:
            Utils.copy_file(cls.filepath_mdl, 'output.mdl', ignore_same_file_error=True)
            Utils.copy_file(cls.filepath_slx, 'original.slx', ignore_same_file_error=True)
            Utils.copy_file(cls.filepath_slx, os.path.join(cls.dirpath_working, 'original.slx'))

        # notify user if preetifying failed.
        if cls._preetify:
            with open(cls.filepath_output_model_only_preetified) as file:
                content = file.read()
                # In case preetifying with TXL fails, nothing is written to output_model_only_preetified.mdl
                if not content:
                    print('\nATTENTIION: Preetifying the output mdl file using TXL grammar failed!!!')
                    print('            Please, discard the preetified version in working directory.\n')


def main():
    def try_transform(args):
        time_start = time.time()
        try:
            Transformer.transform()
            print(f"slx to mdl conversion was successful!\n")

            if args['report_performance']:
                time_taken = time.time() - time_start
                with open(Transformer.filepath_mdl) as file:
                    nlines = len(file.readlines())
                print(f"Output mdl file size : {nlines} lines")
                print(f"Time taken           : {time_taken:.4} seconds")
                # print(f"({nlines}, {int(time_taken * 1000)}),")
        except Exception as e:
            err_msg = "\n*** ERROR: slx to mdl conversion encountered a problem. See details below:\n\n"
            err_msg_print = err_msg + str(e)
            print(err_msg_print)

            err_msg += f"\n\nfilepath_slx                    : {Transformer.filepath_slx}"
            err_msg += f"\nfilepath_mdl                    : {Transformer.filepath_mdl}"
            err_msg += f"\nfilepath_original_mdl, if any   : {Transformer.filepath_original_mdl}"
            err_msg += f"\ndirpath_working                 : {Transformer.dirpath_working}\n"

            err_msg += str(e)

            Utils.log(log_msg=err_msg, log_filepath=Transformer.filepath_error_log, write_mode='append')

            if args['exit_on_failure']:
                sys.exit(1)
        finally:
            Transformer._remove_intermediate_files_and_dirs()

    args = Utils.parse_and_verify_args()

    if args['mode'] == 'single':  # transform only one slx file
        Transformer.initialize(
            args=args,
            filepath_slx=args['slx_filepath'],
            dirpath_working='working-dir',
            dirpath_batch_prod_output=None,
            filepath_mdl=args['mdl_filepath']
        )
        try_transform(args)
        # Transformer.transform()

    else:  # mode = 'batch' : transform all slx files in the folder
        dirpath_slx = args['slx_dirpath']
        filepaths_slx = os.path.join(dirpath_slx, '*.slx')
        filepaths_slx = glob.glob(filepaths_slx)

        if not filepaths_slx:
            print(f"No slx file was found in given slx-dirpath.\n")

        _, slx_foldername = os.path.split(args['slx_dirpath'])
        dirpath_batch_prod_output = f'outputs-{slx_foldername}'
        # we want to make sure dirpath_batch_prod_output is created brand new
        Utils.remove_dirpath(dirpath_batch_prod_output)
        if not args['devt_mode']:
            Utils.create_dirpath(dirpath_batch_prod_output)

        count = 0
        for filepath in filepaths_slx:
            count += 1
            print(f"\ncount: {count}/{len(filepaths_slx)}", end=' ')
            if count < 0:
                print(f"skipping : {filepath}")

            else:
                print(f"================== {filepath} ==================\n")

                dirpath, filename_without_ext, ext_with_dot = Utils.split_filepath(filepath)
                # unlike dirpath_batch_prod_output, dirpath_working is different for each Simulink model
                dirpath_working = f'working-dir-{slx_foldername}/{filename_without_ext}'

                if args['devt_mode']:
                    filepath_mdl = os.path.join(dirpath_working, "output.mdl")
                else:
                    filepath_mdl = os.path.join(dirpath_batch_prod_output, f"{filename_without_ext}.mdl")

                Transformer.initialize(
                    args=args,
                    filepath_slx=filepath,
                    dirpath_working=dirpath_working,
                    dirpath_batch_prod_output=dirpath_batch_prod_output,
                    filepath_mdl=filepath_mdl,
                )
                try_transform(args)

        if not args['devt_mode']:
            Utils.remove_dirpath(f'working-dir-{slx_foldername}')
            Utils.remove_dirpath('working-dir')  # this dir exists if previous transformation was run in 'single' mode

        if args['mode'] == 'batch':
            Utils.remove_file('original.slx')
            Utils.remove_file('original.mdl')
            Utils.remove_file('output.mdl')


def test():
    Utils.log(log_msg='hello there', log_filepath='error-log.txt', write_mode='append')
    # from datetime import datetime
    # x = datetime.now()
    # print(x)


if __name__ == '__main__':
    main()
    # test()
