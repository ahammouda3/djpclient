
def format_data(data):
    '''
    Helper function for properly formatted data to be saved to 
    Session.session_data
    '''
    clean_data = []
    size = len(data)
    for i in range(0,size,4):
        if i+4 < size:
            clean_data.append(data[i:i+4])
            clean_data.append(' \n ')
        else:
            padding = ''
            padsize = size - i
            for k in range(padsize):
                padding += '='
            
            last = data[i:] + padding
            clean_data.append(last)
    
    return ''.join(clean_data)

