def decodeString(s: str) -> str:
    n = len(s)
    stack = []
    for i in range(n):
        if s[i] != "]":
            stack.append(s[i])
        else:
            j = len(stack) - 1
            ss = ""
            si = ""
            found_string = False
            while j >= 0:
                if found_string == False:
                    if stack[j].isalpha():
                        ss = stack.pop() + ss
                    elif stack[j] == "[":
                        stack.pop()
                        found_string = True
                else:
                    if stack[j].isdigit():
                        si = stack.pop() + si
                    else:
                        break
                j -= 1
            ss = int(si) * ss
            stack.extend(ss)
    return "".join(stack)
                


decodeString("3[z]2[2[y]pq4[2[jk]e1[f]]]ef")
