# HardWareSwapGet

This script gets deals, offers, and whatever kind of content from /r/hardwareswap and put its into a ".txt" file and also sends a notification with those deals through email

## Usage

In order to use it (in linux) you'll need to run it as:
```
$ ./HardWareSwapGet.py &
```

If you want to bring it to the foreground just use:
```
$ fg
```

If you want to be able to close that terminal use:
```
$ nohup ./HardWareSwapGet.py &
```

In order to see the process again (but not it's output) use:
```
$ ps aux | grep HardWareSwapGet.py
```
## Email notifications

In order to use your email, you'll have to change the settigns in the HSG.conf file and add your email user and password, aswell as the SMTP server of your email provider.

```
Note: You might have to change your email security settings
```
