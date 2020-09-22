function read_mxarray()

    fid=fopen('original.mdl','r');
    A =fread(fid);
%     disp(A);
    mxArray(A)
end 