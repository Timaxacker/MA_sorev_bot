import traceback
from datetime import datetime
from time import sleep


errorLog = {}
errorLogGlobal = {}
bot = None


class Error:
    def __init__(self, e, error, time, func, args, kwargs, fileName=""):
        self.e = e
        self.error = error
        self.time = time
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.fileName = fileName
        self.errorTextP = ""

    def __str__(self):
        return f"An Error has handled at time: \"{self.time}\":\n+>\"{self.e.__repr__()}\" at line {self.error.lineno} in func \"{self.func.__name__}\" from file \"{self.fileName}\", code:\n+>\"\"\"{self.error.line}\"\"\";\n->with (args, kwargs): {(self.args, self.kwargs)}"


class ErrorLog:
    def __init__(self, _traceback, e, errors=None):
        self.traceback = _traceback
        self.e = e
        self.errors = {} if errors is None else errors

    def __str__(self):
        errorTextP = traceback.format_exception(type(self.e), self.e, self.e.__traceback__)
        errorTextP.reverse()
        i = 0
        for line in errorTextP:
            # print(line)
            if line == "Traceback (most recent call last):\n":
                break
            i += 1
        errorTextP = errorTextP[0:i]
        for i in range(len(errorTextP)):
            if i == 0:
                errorTextP[i] = errorTextP[i][0:len(errorTextP[i])]
            else:
                errorTextP[i] = errorTextP[i][2:len(errorTextP[i])]
        errorTextP.reverse()
        errorText = ""
        for i in range(len(errorTextP)):
            if i % 2 == 1:
                errorText += errorTextP[i]
                if len(keys(self.errors)) >= i // 2:
                    errorThis = self.errors[keys(self.errors)[(i // 2)]]
                    errorText += f"    with (args, kwargs): {(errorThis.args, errorThis.kwargs)}\n    At time: {keys(self.errors)[-i // 2]}\n"
                    # errorText += str(errorThis)
            if i == len(errorTextP) - 1:
                errorText += errorTextP[i]
        return errorText


# def exceptioHandlerBot(func):
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             error = traceback.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
#             #   bot.send_message(args[0].chat.id, "Возникла ошибка. Данные о ней уже отправлены разработчикам.")
#             keyNow = f"\"{datetime.now()}\""
#             errorLog[keyNow] = Error(e, error, keyNow, func, args, kwargs)
#             print(*traceback.format_exception(type(e), e, e.__traceback__))
#             return None
#     return wrapper


def keys(dict_):
    out = []
    if type(dict_) == list:
        return [i for i in range(len(dict_))]
    for i in dict_.keys():
        out.append(i)
    return out


def exceptioHandlerBot(level=1, fileName=""):
    def handler(func):
        def wrapper(*args, **kwargs):
            global errorLog
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error = traceback.TracebackException(exc_type=type(e), exc_traceback=e.__traceback__, exc_value=e).stack[-1]
                keyNow = f"\"{datetime.now()}\""
                q = 0
                while True:
                    try:
                        a = errorLog[f"{keyNow}_{q}"]
                        q += 1
                    except:
                        errorLog[f"{keyNow}_{q}"] = Error(e, error, keyNow, func, args, kwargs)
                        break
                if level == 0:
                    errorTextP = traceback.format_exception(type(e), e, e.__traceback__)
                    errorLog[f"{keyNow}_{q}"].errorTextP = errorTextP
                    errorLogGlobal[f"{keyNow}_{q}"] = ErrorLog(errorTextP, e)
                    errorTextP.reverse()
                    i = 0
                    for line in errorTextP:
                        # print(line)
                        if line == "Traceback (most recent call last):\n":
                            break
                        i += 1
                    errorTextP = errorTextP[0:i]
                    for i in range(len(errorTextP)):
                        if i == 0:
                            errorTextP[i] = errorTextP[i][0:len(errorTextP[i])]
                        else:
                            errorTextP[i] = errorTextP[i][2:len(errorTextP[i])]
                    errorTextP.reverse()
                    errorText = ""
                    for i in range(len(errorTextP)):
                        if i % 2 == 1:
                            errorText += errorTextP[i]
                            if len(keys(errorLog)) > i//2:
                                errorThis = errorLog[keys(errorLog)[i//2]]
                                errorLogGlobal[f"{keyNow}_{q}"].errors[keys(errorLog)[i//2]] = errorThis
                                errorText += f"    with (args, kwargs): {(errorThis.args, errorThis.kwargs)}\n"
                        if i == len(errorTextP) - 1:
                            errorText += errorTextP[i]
                    errorLog = {}
                    print(errorText)
                    send_error(errorText)
                    bot.send_message(args[0].chat.id, "Возикла ошибка. Данные о ней уже отправленны раработчикам.")
                    # print(errorLog)
                    return False
                else:
                    return func(*args, **kwargs)
        return wrapper
    return handler


def send_error(text):
    for id_tg in eval(open('Admins ID.txt', 'r').read()):
        try:
            bot.send_message(id_tg, text)
        except:
            pass


if __name__ == "__main__":
    @exceptioHandlerBot()
    def cab(num):
        sleep(0.1)
        return num/0


    @exceptioHandlerBot()
    def bca(num):
        sleep(0.1)
        return cab(num+1)/0


    @exceptioHandlerBot(level=0)
    def abc(num):
        sleep(0.1)
        return bca(num+1)/0


    print(abc(0))

    print(1)

    print(errorLogGlobal[keys(errorLogGlobal)[-1]])
