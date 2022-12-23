sin = (theta) ->
    switch theta
        when 0 then 0
        when -270, 90 then 1
        when -180, 180 then 0
        when -90, 270 then -1

cos = (theta) ->
    switch theta
        when 0 then 1
        when -270, 90 then 0
        when -180, 180 then -1
        when -90, 270 then 0

rotMatrix = (x, y, z) ->
    [
        [
            cos(y) * cos(z),
            cos(x) * sin(z) + sin(x) * sin(y) * cos(z),
            sin(x) * sin(z) - cos(x) * sin(y) * cos(z)
        ],
        [
            -cos(y) * sin(z),
            cos(x) * cos(z) - sin(x) * sin(y) * sin(z),
            sin(x) * cos(z) + cos(x) * sin(y) * sin(z)
        ],
        [
            sin(y),
            -sin(x) * cos(y),
            cos(x) * cos(y)
        ]
    ]


transformVector = (t, v) ->
    [
        t[0][0] * v[0] + t[0][1] * v[1] + t[0][2] * v[2],
        t[1][0] * v[0] + t[1][1] * v[1] + t[1][2] * v[2],
        t[2][0] * v[0] + t[2][1] * v[1] + t[2][2] * v[2]
    ]


r = rotMatrix(-90, 0, 0)
console.log(r)
v = [3, 4, 0]
console.log(transformVector(r, v))
