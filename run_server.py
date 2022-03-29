import argparse

from server import Gui

if __name__ == '__main__': 
    
    parser=argparse.ArgumentParser()
    parser.add_argument('--filename', help='filename containing data with .hdf5 extension; default: energyNetwork_24h.hdf5',default='energyNetwork_24h.hdf5')
    args = parser.parse_args()

    gui = Gui(args.filename)
    gui.app.run_server(debug=True)
