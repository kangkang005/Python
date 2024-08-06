# 各个 Log 等级的使用
# Verbose: 开发调试过程中一些详细信息，不应该编译进产品中，只在开发阶段使用。
# Debug  : 用于调试的信息，编译进产品，但可以在运行时关闭。
# Info   : 例如一些运行时的状态信息，这些状态信息在出现问题的时候能提供帮助。
# Warn   : 警告系统出现了异常，即将出现错误。
# Error  : 系统已经出现了错误。

#----------------------------------------------------------------------
# logs
#----------------------------------------------------------------------
LOG_ERROR   = lambda *args: print('error:', *args)
LOG_WARNING = lambda *args: print('warning:', *args)
LOG_INFO    = lambda *args: print('info:', *args)
LOG_DEBUG   = lambda *args: print('debug:', *args)
LOG_VERBOSE = lambda *args: print('debug:', *args)

# ignore log levels
# 如果注释下面的 LOG_DEBUG, LOG_DEBUG 将会打印消息；默认关闭 LOG_DEBUG 的消息
# LOG_VERBOSE = lambda *args: 0
LOG_DEBUG   = lambda *args: 0


LOG_VERBOSE("I am verbose")
LOG_DEBUG("I am debug")
LOG_ERROR("I am error")