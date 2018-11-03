; use this file to operate epm in emacs

(autoload 'pymacs-apply "pymacs")
(autoload 'pymacs-call "pymacs")
(autoload 'pymacs-eval "pymacs" nil t)
(autoload 'pymacs-exec "pymacs" nil t)
(autoload 'pymacs-load "pymacs" nil t)
; pymacs-load-path is path for python moudle
(eval-after-load "pymacs"
  '(add-to-list 'pymacs-load-path "~/work/epm"))

; load epmacs.py
(pymacs-load "epmacs")
(pymacs-load "os")

(defun epm-build ()
  "epm build"
  (interactive)
  (save-some-buffers (not compilation-ask-about-save) nil)
  ;;(setq compilation-directory default-directory)
  ;;(setq compilation-directory (epmacs-getprjname)) ; 不好使啊
  (add-to-list 'compilation-search-path (epmacs-getprjname)) ; // https://emacs.stackexchange.com/questions/3895/changing-the-compilation-mode-current-directory-automatically
;;   (compilation-start "epm build"))
  (compile "epm build"))

(defun epm-compile ()
  "epm compile"
  (interactive)
  (save-some-buffers (not compilation-ask-about-save) nil)
  (setq compilation-directory default-directory)
;;   (compilation-start (concat "epm compile " (file-name-nondirectory (buffer-file-name)))))
  (compile (concat "epm compile " (file-name-nondirectory (buffer-file-name)))))

(defun epm-add (filename)
  "epm add"
  (interactive
   (list
    (read-from-minibuffer "Add source file: ")
    ))
  (message filename))

(defun epm-set-active-config (configname)
  "epm set active config"
  (interactive
   (list
    (read-from-minibuffer "Active config name: ")
    ))
  (message configname)
  (epmacs-setactiveconfig configname))

(defvar epm-gdb-args "")
(defun epm-set-gdb-args (args)
  "specify arguments for program"
  (interactive
   (list
    (read-from-minibuffer "Program's args: ")
    ))
  (setq epm-gdb-args args)
  (message args))

(defun epm-show-gdb-args ()
  (interactive)
  (message epm-gdb-args))

(defvar epm-gdb-dir ".")
(defun epm-set-gdb-dir (args)
  "specify gdb's working dir"
  (interactive
   (list
    (read-from-minibuffer "change gdb default directory: ")
    ))
  (setq epm-gdb-dir args)
  (message args))

(defun epm-show-gdb-dir ()
  (interactive)
  (message epm-gdb-dir))

(defun epm-run-gdb ()
  "epm run gdb"
  (interactive)
  (os-chdir (expand-file-name default-directory))
  (gdb (concat (if (> emacs-major-version 21)
                   ;; "gdb --annotate=3 -cd . --args debug/"
                   ;; (concat "gdb --annotate=3 -cd "
                   (concat "gdb -i=mi -cd "
                           epm-gdb-dir
                           ;; " --args debug/")
                           " --args ")
                 "gdb -cd . --args debug/")
               (epmacs-getexename) " " epm-gdb-args)))

(defun foo ()
  "foo"
  (interactive)
  (message "foo is %d" (epmacs-foo 8)))

(global-set-key "\C-cc" 'foo)
(global-set-key [f7] 'epm-build)
(global-set-key [C-f7] 'epm-compile)
(global-set-key [f5] 'epm-run-gdb)

(provide 'epmacs)
