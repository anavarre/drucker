set shell=/bin/bash

" No need to have VIM compatible with VI
set nocompatible

filetype plugin indent on

" Pathogen integration
execute pathogen#infect()

" Leader
let mapleader = ","
let maplocalleader = "\\"

" Security enhancement
set modelines=0

set encoding=utf-8
set ffs=unix,mac,dos " Use Unix as the standard file type
set scrolloff=7 " Number of lines to scroll up or down
set autoindent
set showmode
set showcmd
set hidden
set wildmenu
set wildmode=list:longest
set visualbell
set cursorline
set ttyfast
set ruler " Always show current position
set backspace=indent,eol,start
set laststatus=2
set number " Show line number
set ruler "Always show current position
set clipboard=unnamed " Use the system clipboard

" Developer experience improvements, with auto-closing elements.
"inoremap ( ()<Esc>i
"inoremap [ []<Esc>i
"inoremap { {}<Esc>i
"inoremap " ""<Esc>i
"inoremap ' ''<Esc>i

" NERDTree-like browser
let g:netrw_banner = 0
let g:netrw_liststyle = 3
let g:netrw_browse_split = 4
let g:netrw_altv = 1
let g:netrw_winsize = 25

" vim-gitgutter
set updatetime=250 " reduce gutter update time to 250ms

" Re-mapping
map <C-\> :Vex<CR>
map <F3>  :set paste<CR><Esc>i
map <F6>  :tabp<CR>
map <F8>  :tabn<CR>
map <F9>  :set number!<CR>
map <leader>l :set list!<CR>
imap <F10> <C-x><C-o>

" Tab management
set tabstop=2
set softtabstop=2
set shiftwidth=2
" Use spaces instead of tabs
set expandtab

set ai "Auto indent
set si "Smart indent
set wrap "Wrap lines
set linebreak " Do not cut words at the end of line
" set showbreak=...

" Search improvements
set ignorecase " Ignore case when searching
set smartcase  " When searching try to be smart about cases
set hlsearch   " Highlight search results
set incsearch  " Makes search act like search in modern browsers
set showmatch  " Show matching brackets when text indicator is over them
set gdefault   " Apply substitutions globally on lines

" Color scheme
syntax on
colorscheme Tomorrow

" Autosave files on every keystroke.
autocmd TextChanged,TextChangedI <buffer> silent write

" Drupal files must be highlighted as PHP files
if has("autocmd")
  augroup module
    au! BufRead,BufNewFile *.module set filetype=php
    au! BufRead,BufNewFile *.install set filetype=php
    au! BufRead,BufNewFile *.test set filetype=php
    au! BufRead,BufNewFile *.inc set filetype=php
    au! BufRead,BufNewFile *.profile set filetype=php
    au! BufRead,BufNewFile *.view set filetype=php
    au! BufRead,BufNewFile *.theme set filetype=php
    au! BufRead,BufNewFile *.engine set filetype=php
  augroup END
endif

" Twig syntax highlighting
au! BufRead,BufNewFile *.twig set filetype=jinja

" PHP OmniCompletion
autocmd FileType php set omnifunc=phpcomplete#CompletePHP

" Ignore the below filetypes
set wildignore+=*.exe,*.dll " Windows binaries
set wildignore+=*.jpg,*.jpeg,*.png,*.gif,*.bmp,*.tga,*.mp3,*.ico,*.wav " Media files
set wildignore+=.hg,.git,.svn " VCS files and directories
set wildignore+=*.pdf,*.doc,*.docx,*.xls,*.xlsx " Binary document formats
set wildignore+=.DS_Store " Mac OSX metadata files
set wildignore+=*.lnk " Windows metadata files
