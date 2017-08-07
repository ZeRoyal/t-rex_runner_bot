import win32api as wapi
import win32con as wc


keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.';$/\\":
    keyList.append(char)

def key_check():
    keys = []
    if wapi.GetAsyncKeyState(wc.VK_LEFT) != 0: 
        return ['left']  
    elif wapi.GetAsyncKeyState(wc.VK_RIGHT) != 0: 
        return ['right'] 
    elif wapi.GetAsyncKeyState(wc.VK_UP) != 0: 
        return ['up'] 
    elif wapi.GetAsyncKeyState(wc.VK_DOWN) != 0: 
        return ['down'] 
    
    else:      
        for key in keyList:
            if wapi.GetAsyncKeyState(ord(key)):
                keys.append(key)
        return keys
    

        
 