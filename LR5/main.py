import process
import input_data

if __name__ == '__main__':
    data = input_data.get_data()
    p = process.find_p(data)
    print("p = ", p)
