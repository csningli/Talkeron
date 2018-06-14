#ifndef CMDCOMPILERESULT_H
#define CMDCOMPILERESULT_H

#include "taskblock.h"

class CmdCompileResult
{

private :
    bool compiled;
    QString comment;

public:
    CmdCompileResult();

    bool setCompiled(bool b);
    bool getCompiled();

    bool setComment(QString cm);
    QString getComment();

};

#endif // CMDCOMPILERESULT_H
