import process

if __name__ == '__main__':
    data = process.get_data()
    p = process.find_p(data)
    print("p = ", p)