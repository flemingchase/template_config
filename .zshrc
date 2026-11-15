HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
setopt autocd
unsetopt beep
bindkey -v
zstyle :compinstall filename "${ZDOTDIR:-$HOME}/.zshrc"

autoload -Uz compinit && compinit
zstyle ':completion:*' matcher-list '' 'm:{a-zA-Z}={A-Za-z}'

if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias dir='dir --color=auto'
    alias vdir='vdir --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

PS1='%F{cyan}%n%F{default}:%F{magenta}%~%F{green}> %f'

alias c="clear"
alias list_font="fc-list : family | sort -u"
alias dropbox="dropbox-cli"
alias zathura="fzathura"
alias la="ls -a"
alias ll="ls -l"
alias lla="ls -la"
alias lsd="ls -d */"
alias ga="git add"
alias gc="git commit"
alias gp="git push"

export PATH="$HOME/.local/bin:$PATH"
export EDITOR=vim

# Use the bundled Gotham palette for Qt applications.
if (( $+commands[qt6ct] )) && [[ -r ${XDG_CONFIG_HOME:-$HOME/.config}/qt6ct/qt6ct.conf ]]; then
    export QT_QPA_PLATFORMTHEME=qt6ct
fi

fzathura() {
    emulate -L zsh
    local file

    if [[ -f ${1:-} ]]; then
        file=$1
        shift
    else
        file=$(find "$HOME" -type f | fzf) || return
    fi
    [[ -n $file ]] || return 0

    # &! starts a detached job without relying on a particular job number.
    nohup zathura "$@" "$file" </dev/null >/dev/null 2>&1 &!
}

screenshot() {
  emulate -L zsh

  local delay=${1:-0}
  local directory="$HOME/screenshots"

  if [[ "$delay" != <-> ]]; then
    print -u2 "Usage: screenshot [delay in seconds]"
    return 1
  fi

  mkdir -p -- "$directory" || return

  local filename="$directory/$(date '+%Y-%m-%d_%H-%M-%S')_full.png"

  command scrot --count --delay="$delay" "$filename"
}

printcolors() {
    emulate -L zsh
    local -a names=('Black' 'Red' 'Green' 'Yellow' 'Blue' 'Magenta' 'Cyan' 'White')
    local i
    printf '\e[39mDefault foreground\e[0m  \e[49mDefault background\e[0m\n'
    for i in {1..8}; do
        printf '|%03d| \e[%dm%-8s\e[0m |%03d| \e[%dm%-8s\e[0m |%03d| \e[%dmBright %-8s\e[0m |%03d| \e[%dmBright %-8s\e[0m\n' \
            $((29+i)) $((29+i)) "$names[i]" \
            $((39+i)) $((39+i)) "$names[i]" \
            $((89+i)) $((89+i)) "$names[i]" \
            $((99+i)) $((99+i)) "$names[i]"
    done
}

(( $+commands[rbenv] )) && eval "$(rbenv init -)"
export WORKON_HOME="$HOME/.virtualenvs"
[[ -r /usr/bin/virtualenvwrapper.sh ]] && source /usr/bin/virtualenvwrapper.sh

