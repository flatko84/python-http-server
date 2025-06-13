from hooks.send import compression

hooks = {
    "receive": [

    ],
    "send": [
        compression.Compression
    ]
}