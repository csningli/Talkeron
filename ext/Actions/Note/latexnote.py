#! /usr/bin/

if __name__ == "__main__" :
    import sys, os, subprocess, time
    sys.path.append("/Users/nil/.talkeron/Actions/Common")
    import utils 
    
    print("Execution of latexnote.py started.")
    
    success, workPos, parasDic = utils.handle_sys_argv(sys.argv)
    
    if success is not True : 
        exit(1)
        
    takeronHome = parasDic.get("talkeron", None)
    noteDir = parasDic.get("directory", None)
    noteName = parasDic.get("notename", None)
    
    if noteDir is not None and os.path.isdir(noteDir) :
        print("Note directory: ", noteDir)
    else :
        print("Exit. [Input parameter \"directory\" is missing or inavailable.]")
        exit(1)

    notePath = noteDir + "/" +  time.strftime("%y%m%d%H%M%S") + "-" + noteName
    if notePath is not None and not os.path.isdir(notePath) :
        print("Note path: ", notePath)
    else :
        print("Exit. [Note path : " + notePath + " already exist.]")
        exit(1)
    
    os.mkdir(notePath)
    os.chdir(notePath)
    
    with open("./" + noteName + ".tex", 'w') as f :
        f.write("\\documentclass{article}\n")    
        f.write("\\usepackage[top=1.5cm,bottom=1.5cm,left=1.5cm,right=1.5cm]{geometry}\n")
        
        # add configurations to the file 
        
        f.write("%\n")
        f.write("%\n")
        f.write("\\usepackage{amsmath}%\\allowdisplaybreaks[4]\n")
        f.write("\\usepackage{amsthm}\n")
        f.write("\\usepackage{amsfonts}\n")
        f.write("\\usepackage{amssymb}\n")

        # add graphic configurations to the file 

        f.write("\\usepackage{graphicx}\n")
        f.write("\\usepackage[sl]{caption}\n")
        f.write("\\usepackage{color}\n")

        # add algorithm configurations to the file 
        
        f.write("\\usepackage{listings}\n")
        f.write("\\usepackage[ruled,vlined]{algorithm2e}\n")
        f.write("\\usepackage{hyperref}\n")
        f.write("\\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=red,linktoc=all}\n")
        
        # sample definitions for newtheorem

        f.write("%\n")
        f.write("%\n")
        f.write("%\\newtheorem{theorem}{\\hskip\\parindent Theorem}\n")
        f.write("%\\newtheorem{lemma}{\\hskip\\parindent Theorem}\n")

        # sample definitions for newcommand

        f.write("%\\newcommand{\\abstractname}{abstract}\n")

        # sample definitions for symbols

        f.write("%\\newcommand{\\ftwo}{\\frac{1}{2}}\n")

        # personalized note form
        
        f.write("%\n")
        f.write("%\n")

        f.write("\\newcommand{\\ignore}[1]{}\n")
        f.write("\\newcounter{note}[section]\n")
        f.write("\\renewcommand{\\thenote}{\\thesection.\\arabic{note}}\n")
        f.write("\\newcommand{\\li}[1]{\\refstepcounter{note}$\\ll ${\\sf Li's Comment~\\thenote:}\n")
        f.write("{\\sf \\textcolor{blue}{#1}}$\\gg$\\marginpar{\\tiny\\bf LC~\\thenote}}\n")

        # begin the document

        f.write("\\begin{document}\n")
        f.write("\n")
        f.write("\n")
        f.write("\\rightline{\\bf NiL,~~\\tt{csningli@gmail.com}}\n")
        f.write("\\vspace{0.3cm}\n")
        f.write("\\noindent{\\Large\\bf Note: " + noteName + "}\n")
        f.write("\\vspace{0.5cm}\n")
        f.write("\\newline\\textbf{Abstract.} abstract here.\n")
        f.write("\n")
        f.write("\n")
        f.write("\\vspace{0.2cm}\n")
        f.write("\\hrule height 2pt\n")
        f.write("\n")
        f.write("\n")
        f.write("%\\vspace{1cm}\n")
        f.write("%\\tableofcontents\n")
        f.write("\\vspace{1cm}\n")
        f.write("Content here.\n")
        
        # end the document

        f.write("\\end{document}\n")

        # samples that does not appear

        # sample reference  
        f.write("%\n")
        f.write("%\n")
        f.write("%\\label{Bibliography}\n")
        f.write("%\\noindent\\textbf{\Large Bibliography}\n")
        f.write("%\\bibliographystyle{plain}\n")
        f.write("%\\bibliography{Bibliograpy} % which refer to the file Bibliograpy.bib\n") 
 
        f.write("%\n")
        f.write("%\n")
        f.write("%\\begin{thebibliography}{1}\n")
        f.write("%\\vspace*{-6pt}\n")
        f.write("%\n")
        f.write("%\\bibitem{REF}\n")
        f.write("%A. Author, and B. Author\n")
        f.write("%\\newblock title.\n")
        f.write("%\\newblock In {\em {CONF} '15, 2015}.\n")
        f.write("%\\end{thebibliography}\n")
        
        # sample figure

        f.write("%\n") 
        f.write("%\n")
        f.write("%\\begin{figure}[!htb]\n")
        f.write("%\\begin{minipage}[t]{0.8\\textwidth}\n")
        f.write("%\\centering\n")
        f.write("%\\includegraphics[width=0.3\\textwidth]{fig.pdf}\n")
        f.write("%\\caption{caption}\n") 
        f.write("%\\label{fig}\n")
        f.write("%\\end{minipage}\n")
        f.write("%\\end{figure}\n")

        # sample algorithm

        f.write("%\n")
        f.write("%\n")
        f.write("%\\begin{algorithm}\n")
        f.write("%\\textbf{Initialization:} \\\\ \n")
        f.write("%\\nl $p(v) := q(v) := \\zeta$; \\\\ \n")
        f.write("%\\nl	\\If{condition}{\n")
        f.write("%\\nl		statement; \\\\ \n") 
        f.write("%}\n")
        f.write("%\\nl	\\Else{\n")  
        f.write("%\\nl		statement; \\\\ \n")
        f.write("%}\n")
        f.write("%\\vspace{0.2cm}\n")
        f.write("%\\nl	\\lIf{condition}{statement;}\n")
        f.write("%\n")
        f.write("%\\caption{caption}\n")
        f.write("%\\label{algo}\n")
        f.write("%\\end{algorithm}\n")

        # sample listing

        f.write("%\n")
        f.write("%\n")
        f.write("%\\begin{lstlisting}[language=C++,frame=single,caption={caption}]\n")
        f.write("% statement\n")
        f.write("%\\end{lstlisting}\n")
        f.write("%\\lstinputlisting[language=C, firstline=1, lastline=10, numbers=left]{source.c}\n")

        # sample table

        f.write("%\n")
        f.write("%\n")
        f.write("%\\begin{table}[!htp]\n")
        f.write("%\\centering\n")
        f.write("%\\begin{tabular}{|c|c|}\n")
        f.write("%\\hline\n")
        f.write("% 1.0 & 1.0 \\\\ \n")
        f.write("% 1.0 & 1.0 \n")
        f.write("%\\hline\n")
        f.write("%\\end{tabular}\n")
        f.write("%\\caption{caption}\n")
        f.write("%\\label{tab}\n")
        f.write("%\\end{table}\n")
        
        print("Now you can edit the note.")

        cmd = "open " + notePath
        subprocess.call(cmd, shell = True)
    
    print("Done.")
