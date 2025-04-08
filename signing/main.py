import tkinter as tk

from frames.usb_check import GetKeyFromUSBFrame
from services.pdf_signer import signer

APP_WIDTH = 800
APP_HEIGHT = 600
APP_TITLE = 'TEST APP'

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Basic configuration
        self.title(APP_TITLE)
        self.geometry(f'{APP_WIDTH}x{APP_HEIGHT}')
        self.resizable(False, False)

        self.current_frame = GetKeyFromUSBFrame(self, self.get_key_from_usb_result)
        self.current_frame.pack(fill='both', expand=True)

    def get_key_from_usb_result(self, key: str):
        # self.current_frame.destroy()
        # self.current_frame = GetKeyFromUSBFrame(self, lambda test: print(test))
        # self.current_frame.pack(fill='both', expand=True)
        print(key)


if __name__ == "__main__":
    # App().mainloop()
    priv_key = """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"""

    public_key = """MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAvbFeA6XBmxeXJvHBITRX
hEVdUtg5Mohm1ePkd34QmJ5ej/F6GAXeYf0LdyrEN93QTaWbdcg3eJZFaZX7lKTZ
GQoNFjbXRxC5rtieb+oPud0gwahXuQ9/XLTC3dI+WgCMnxn4KR4PnlBeOmmoiedg
UED/tE4p7DEuwu+HcCFgxCgy8OhO5Y2e81mGEhUvcUtMrtC5VQDFTNl/HxjE6m09
wC62FSGN+WDxofzNvRKeNubmLkHS80c1jMY2PdY5mTPgF9VSrYSu0lh1vNophM9g
DYgm6rVM8nXBOm8cUQSoay9/Ipsr/1mE2FTvhkTDesoJdwnQ2GptvbDRHk/+9K4r
zObygMNNqS8ZvCfdgBaWZRYtokVXI8zax/Fo4DvABPNqnRh73xTZ4Lv/T2TGO26C
/6UPjF154C6R3Gex4Wh9Yyc5PtRvj91hAT/RG9GLbSrIXPs+mkv8DftIYFhckCUw
m/rCNNMehPtpHG7MXbXwoLSJtDfZll0uIdnIGFHmpRCx+PEgcESzSqH18kfwjtsb
KPQ7bxOpDIBWBF5G7zBz7kugVSAu/94WjFMTnJ5eXIjG8mylOf5iof9VFPVXwhC3
NAPXrmhCHYWaxkDV6OU59XnoBJXe3V0OkYlRH3EWkVrPJYPJE5gc14YIRVoEhCxA
A1qiCWP4ZeALrHK+NF/aPuECAwEAAQ=="""
    signer.sign(priv_key, "/home/pawel/Desktop/test.pdf")
