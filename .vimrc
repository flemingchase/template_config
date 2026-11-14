filetype plugin indent on
filetype plugin on
syntax enable
set nocompatible
set showmatch
set ignorecase
set nohlsearch
set incsearch
set tabstop=4
set softtabstop=4
set expandtab
set shiftwidth=4
set autoindent
set number
set wildmode=longest,list
set textwidth=79
set cc=80
set relativenumber
set formatoptions+=t
set mouse=a
set clipboard=unnamedplus
set cursorline
set ttyfast
set noswapfile
set conceallevel=0
set nowrap
set splitright

let maplocalleader=","
noremap <LocalLeader>sh :split<CR>
noremap <LocalLeader>sv :vsplit<CR>
noremap <silent> <c-h> <c-w>h
noremap <silent> <c-j> <c-w>j
noremap <silent> <c-k> <c-w>k
noremap <silent> <c-l> <c-w>l
noremap <LocalLeader>V :Vex<CR>

autocmd BufRead *.md,*.markdown,*.rst set filetype=markdown
autocmd BufWritePre * keeppatterns %s/\s\+$//e
highlight QuickFixLine gui=bold,underline cterm=bold,
            \underline guibg=NONE ctermbg=NONE guifg=NONE

augroup ColumnExceptions
  autocmd!
  autocmd FileType markdown,text,tex,plaintex setlocal colorcolumn= textwidth=0
augroup END

if empty(v:servername) && exists('*remote_startserver')
      call remote_startserver('VIM')
endif

" Vimtex settings
autocmd ColorScheme * highlight link texMathOper Normal
noremap <LocalLeader>lC :VimtexClean!<CR>
let g:tex_flavor='latex'
let g:vimtex_view_method = 'zathura'
let g:vimtex_view_use_temp_files = 1
let g:vimtex_compiler_latexmk = {
      \ 'options' : [
      \   '-verbose',
      \   '-emulate-aux-dir',
      \   '-file-line-error',
      \   '-synctex=1',
      \   '-interaction=nonstopmode',
      \ ],
      \}
let g:vimtex_quickfix_ignore_filters = ['Underfull', 'Overfull',]

" Airline-theme
let g:airline_theme='minimalist'

" Plugins
call plug#begin()
" Make sure you use single quotes
Plug 'lervag/vimtex'
Plug 'bling/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'SirVer/ultisnips'
call plug#end()
