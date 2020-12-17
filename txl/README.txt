The contents of this directory are required only for preetifying the output mdl file (based on TXL grammar)
Due to the unupdated TXL grammar, output mdl files were found to be corrupted when preetifying them this way i.e. using TXL.
So, this feature i.e. preetying the output mdl file is turned off (by setting 'preetify' to False in Transformer.initialize()).
However, the code to preetify is still there. So, we are still keeping this directory. 

This directory i.e. txl can be removed if the corresponding code for preetying mdls is removed. 
