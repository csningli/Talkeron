#include "cmdcompileresult.h"

CmdCompileResult::CmdCompileResult()
{
    compiled = false;
    comment = "";
}

bool CmdCompileResult::setCompiled(bool b) {
    compiled = b;
    return true;
}

bool CmdCompileResult::getCompiled() {
    return compiled;
}

bool CmdCompileResult::setComment(QString cm) {
    comment = cm;
    return true;
}

QString CmdCompileResult::getComment() {
    return comment;
}

