import sys, tty, select, termios



class KeyBoard(object):

    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def get_key(self):
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return ""

    def get_kbd(self):
        b=[0,0,0]
        b[0] = self.get_key()
        
        if b[0] == "":
            return ''
        
        if b[0] == '\x1b':
            b[1] =self.get_key()
            b[2] =self.get_key()
            if b[1]=="" :
                k=ord(b[0])
            elif b[2]=="":
                k= ord(b[1])
            else :
                k= ord(b[2])       
        else:
            k = ord(b[0])

        key_mapping = {
        127: 'backspace',
        10: 'return',
        32: 'space',
        9: 'tab',
        27: 'esc',
        65: 'up',
        66: 'down',
        67: 'right',
        68: 'left'
        }
        return key_mapping.get(k, chr(k))


if __name__ == '__main__':
# Use like this
    with KeyBoard() as kb:
        i = 0
        print("Type:")
        while 1:
            ch = "" + kb.get_key()

            if ch == '\x1b':  # x1b is ESC
                break
            
            if (ch != "") :
                print(ch.upper(), end='')

        i = 0
        print("Type:")       
        while 1:
            c = kb.get_kbd()
            if c != '' :
                print(c)
            if c == 'esc': 
                break

                    
                     
