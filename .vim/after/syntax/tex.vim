" ~/.vim/after/syntax/tex.vim
" Non-destructive math regions for custom environments:
"   \be ... \ee
"   \be* ... \ee*
"   \ba ... \ea
"   \ba* ... \ea*
" The regions do NOT redefine the canonical texMathZone; they allow the
" existing math clusters to operate inside, preserving all math highlighting.

if exists('b:current_syntax') && b:current_syntax ==# 'tex'
  " Clear any previous trial definitions to allow safe reloads
  silent! syntax clear texBeMath
  silent! syntax clear texBaMath

  " Common contains list: prefer the cluster; fall back to commonly used groups.
  " Extend this list with any additional group names shown by ":syntax list".
  let s:math_contains = '@texMathZone,texMathOper,texMathDelim,texMathSuperSub,texMathSymbol,texMathFunction,texMathSub,texMathSuper'

  " \be ... \ee and \be* ... \ee*
  syn region texBeMath
        \ matchgroup=Delimiter
        \ start='\\be\%(\*\)\?\>'
        \ end='\\ee\%(\*\)\?\>'
        \ keepend contains=@texMathZone,texMathOper,texMathDelim,texMathSuperSub,texMathSymbol,texMathFunction,texMathSub,texMathSuper

  " \ba ... \ea and \ba* ... \ea*
  syn region texBaMath
        \ matchgroup=Delimiter
        \ start='\\ba\%(\*\)\?\>'
        \ end='\\ea\%(\*\)\?\>'
        \ keepend contains=@texMathZone,texMathOper,texMathDelim,texMathSuperSub,texMathSymbol,texMathFunction,texMathSub,texMathSuper

  " Make both regions visually use the usual math highlighting
  hi def link texBeMath texMathZone
  hi def link texBaMath texMathZone
endif

