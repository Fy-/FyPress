import sys
from fypress import app

def main():
    app.run(host='0.0.0.0', debug=True)
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit()