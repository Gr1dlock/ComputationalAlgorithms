import process
import io

if __name__ == '__main__':
    data = io.get_data()
    p = process.find_p(data)
    print("p = ", p)
