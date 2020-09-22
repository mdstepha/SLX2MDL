include "grammars/mdl.grm"
include "grammars/addons.grm"

rule main 
    replace $ [program]
        P [program]
    by  
        P 
end rule 