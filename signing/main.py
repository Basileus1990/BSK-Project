import tkinter as tk

from cryptography.hazmat.primitives import serialization

from frames.usb_check import GetKeyFromUSBFrame
from services.pdf_signer import sign, verify

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
    App().mainloop()
#     priv_key = """-----BEGIN RSA PRIVATE KEY-----
# MIIJKAIBAAKCAgEAlCccxGWuhMwEfIBPfavOudY8M0UjIha2TkRimj8Sx3AA3ToS
# QmNZew67npbL99lAVJKbYeQaGe//3RJJ87PE0+zQsmi/bPJhmFKbVai2C0SRQi8n
# 10R7MgG4BKuzy8Rt5hkIFelj/66uFSRw1EIm5z1Tx3B3FYl5Tt6a/Tetefdo5trT
# 0ED1yddph2m9Hy4/wCXjlPCWyIBckuAVNI5qCJC6ChkLpbD+90bFu7V6LAgjWcPh
# Fzne1HNH9gZMsaa5j1L9j5ppQBVlS7UY1GE93WUbm8Zuva8IDXCZ15VzIsHRqzJj
# kIDhjQrl9BrsjNfR4rj3kEzoyxpIYllM6jlAskpEkaiU21vW8/drjjbi1rWuTnbR
# hTVtx4KTpyztQb6KMTzPVJ0nMesjBorAnQXpi85wrs9PNs3gyHxXcqoJhplqSQzu
# 5UQX9baiCKeX6LYvTX2f1oTaN9rHuUKnYCrlJjdGyT1371ctg+Dbv1vhU/bRdDhA
# 0cYTtoZxuFGM1GKXRkFyf6/QM6gQKGWkCCGtbtQ0nAea+rJwdiqsoXseqoLMJmod
# hziGpqk9lF9Ups8bYAK1yrkZC9ALlCcTkgMNBxoRLriapgBGLqMMbPwWAL3INWQE
# ZgJyfIe293YrdzS6+wG/+0Enht+ieCuI9DBpGd8hbTS/RaakUlfy7PQKl3sCAwEA
# AQKCAgBIXJo2axvEjQmb7eflj+cW6cbZm+k/GyzMKaanhCsd8lzZsSV9+5yW+Gk3
# WpwhYKGFLV5rf8gn5wtn5SjtuV5nzIFawsLM6c41YhOw0QiplEIGu5WQFUi+8gv5
# bAwTeMvc2VkTqr1HAwDQHs5lPjJWO6QSA6KGiHERzrSQ/YLj0a4RI8zVKQVkIqzO
# kRzof+Rva5IvCxv6roeIzZ5N30l3CYl0qSsBMOQ3zv+BYXBc1VS+4WetunxV9ECv
# sAABvVdg474pR9gkjs69HaUVBrH60wmbGl64kycxuU/K9poX3ecU4TW0PN7tzubm
# RchIOpmvTXzNpGMH4Lx+HPPuayxno+tT8vPMNJHPJdn91W26otMYvgwVF80Awhwv
# 2eimtZXmrK3qaEh+7JtBQI0kbnAccR748Vg1cHxD5yjYnLMwzfpnXjLJlhGmV4D7
# qKCmZ6psArtpAqRs6eTF+Nk56/qcyB0YuxuCExFieZZs2kUvakCcOhgfH6djL2eO
# DKtMZJP7zcA+qCpPV4/nnvKk6hawMElcTC9lWMSjwBTWhP+CP51BHL0OAF4x0XfZ
# thKCHlCs929YohAuExUsWQBFU8KIzNKQqyjTmGKZ9UCs0U2aMLTE+KYFT6xoeEK5
# GJyed3WuGaoG8XwndBtOuoM9W4jWLc9YYQNeNM36QdIKFWPB4QKCAQEA/YwpsrM1
# i+yuy7XScAtrfiFra860PqmFFUw2Ox7Q9iKDHcLMtevRaY5Sa1vyx29LQnxJxlku
# rxkdfGBEbv5KP8C5oZnmmAvqFfmLbeo83YIEMaQG3+smBIoMmCQPareb1w3d7t2z
# xsIv/31jRWFe4ZUhPS+LOpxJ+8y+MxkRvvJry8L+OPhvDouTVe0dx/oJpE9TBfgM
# /6nIK91xwzdM9SN9Wb5OPEJ4vArlX1Wv5nLGaqXwWIryS0SqbgLTrKFAOk4uVoB5
# gAfyn+Ek8VNClj8cS3wyzO6sIl09tmlEIaUCNk/FDMqeG1tTpLs/zY68OyunW9ty
# sNUUePV5iT8ycwKCAQEAlZX4TBCFEUVEnRbfqHyI4h+IU4J+yFUW+b1XNTSQTp06
# tnPyI/UuZqjsI4AzVy98BbKCwE10QcNtGpNC+tNWURhpK59nwJtTSr0Ij5XIUKH/
# FjaL/Ci8Noygexw0mxjiiNWp1n585iw7JPC14NYXy+4rMg419bOCsDX1yFMGqr4j
# blfuCPcncybj3KgGcp/IfgTSmVn6oxGxLC60KIY72+DcbIio5BzAD0EFjK+s/UUR
# np4MTWL1xpYh/e9X46yJQB7lmAJqS8MN3jMWHy7XT+Y1H6yCToiIC4+eLdKNw/1H
# coVmdyIev2ziW1A5kgE0NU94pwkZQcCZBzcQy+rc2QKCAQB9kJR181ppWWWXbQwy
# gPVTGanhUhThk4Jc8clJrhE+VAkrC/XlgkvLQrh+gqLRMcTLwFGo8TG1dXKszeAW
# N8j9maxU46rXUc8z4smyPXa3HFSHYPwmmIXTaaqjDfi0mQmMj0mBqjoGDNVIaghn
# q7kZbolvi8Qf2papJNRs6dVoAxZvaroL7LzTLzxgKXW+O43a2Y38PsPxOVvwnVJh
# o1lxbYn+j8ie/yxbs+m0NPNP5TduSY+lyeoEbJUatjuuGo18UouQOz/wr/7wPsfU
# 2672SXrxxyhBZVHKEvMlCyy6nMVjsE2d8Bos4iWiRzlpy25cv1m6nAtIl73zyV3P
# IoURAoIBAGOPDFJ8EETdaHxxc+zs7iIqQI7sZLurPn570aY81Ost5Jz48KmUDw0O
# 0xQRyJn3pcEY/cNGCeGXU2+DoenVbTbOW3lIQELGXpp41FDUrR1VpLTBG0x6REK+
# ODWYIT81Qdk29DIpv7FmsPq2Jyd89xuo6iEHqkxc7NehInPxJpfPsz9G0Mwwy5Xt
# xWzgfGIgDM4rIYwlgha0uMoiT5BFP2Pp9mtaTaZ9qCq+6RWo+ycaqE58/M0o11IU
# LI2ZllKXTEZcCg2xVdQU/47rS4b3oyCvpJ3vME9aucmQDgSLhgVy9vG27erOz84y
# hzmlXJvbp0bwHOp3uNK1gGR39vrx14kCggEBAJSfTR0NiWMuhcpys+yE1Lgp1bAA
# Kq6HtIp7zZubavtTCGYhzrvQ4yMaeJrrax5HIh9mPvBPoPxl45b64pDk2+TJbtOK
# FqYkRikAqe9W+DSVL93WikmewPhejFoJxJSU1hU6B4JoSrwyCc3tuPEHDb29F2O4
# lrN0zKV6o/SptuqcVRReVi4LOgyjOxsqpZ10oDhfK/i1zV2Ycr3qldeX7Zo4kmOv
# 5q6vm8DzTqdKnA3R/yKVMYvYemd26Y9xs9nN1C6aWMMiLfHV9bwLY9qJtPpw6Xfx
# ifVQOAodQ4jmVZujNnp5yNydJOcbstIZbsmHpOn/+3TrGcBacOed0fD89Lo=
# -----END RSA PRIVATE KEY-----"""
#
#     public_key = """-----BEGIN PUBLIC KEY-----
# MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAlCccxGWuhMwEfIBPfavO
# udY8M0UjIha2TkRimj8Sx3AA3ToSQmNZew67npbL99lAVJKbYeQaGe//3RJJ87PE
# 0+zQsmi/bPJhmFKbVai2C0SRQi8n10R7MgG4BKuzy8Rt5hkIFelj/66uFSRw1EIm
# 5z1Tx3B3FYl5Tt6a/Tetefdo5trT0ED1yddph2m9Hy4/wCXjlPCWyIBckuAVNI5q
# CJC6ChkLpbD+90bFu7V6LAgjWcPhFzne1HNH9gZMsaa5j1L9j5ppQBVlS7UY1GE9
# 3WUbm8Zuva8IDXCZ15VzIsHRqzJjkIDhjQrl9BrsjNfR4rj3kEzoyxpIYllM6jlA
# skpEkaiU21vW8/drjjbi1rWuTnbRhTVtx4KTpyztQb6KMTzPVJ0nMesjBorAnQXp
# i85wrs9PNs3gyHxXcqoJhplqSQzu5UQX9baiCKeX6LYvTX2f1oTaN9rHuUKnYCrl
# JjdGyT1371ctg+Dbv1vhU/bRdDhA0cYTtoZxuFGM1GKXRkFyf6/QM6gQKGWkCCGt
# btQ0nAea+rJwdiqsoXseqoLMJmodhziGpqk9lF9Ups8bYAK1yrkZC9ALlCcTkgMN
# BxoRLriapgBGLqMMbPwWAL3INWQEZgJyfIe293YrdzS6+wG/+0Enht+ieCuI9DBp
# Gd8hbTS/RaakUlfy7PQKl3sCAwEAAQ==
# -----END PUBLIC KEY-----"""
#
#     public_key_bytes = priv_key.encode('utf-8')
#     private_key_obj = serialization.load_pem_private_key(
#         public_key_bytes,
#         password=None,  # Assuming unencrypted key as per function signature
#     )
#
#     public_key_bytes = public_key.encode('utf-8')
#     public_key_obj = serialization.load_pem_public_key(
#         public_key_bytes,
#     )
#     sign(private_key_obj, "/home/pawel/Desktop/test.pdf", "/home/pawel/Desktop/test-out.pdf")
#     print(verify(public_key_obj, "/home/pawel/Desktop/test-out.pdf"))
