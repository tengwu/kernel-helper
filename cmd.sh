# find symbols
find . -iregex ".*\.[cs]" -not -path "./drivers/*"|xargs grep "asm_exc_divide_error" --color -n
