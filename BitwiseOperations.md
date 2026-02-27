# BitWise Operations

Here's a quick explanation of bitwise operations used to get the base64 string:

### The operations

| Operator | Name | Description |
|---|---|---|
| & | Bitwise AND | Sets a bit to 1 if both corresponding bits are 1, otherwise 0. Used for checking or clearing bits. |
| \\| | Bitwise OR | Sets a bit to 1 if at least one corresponding bit is 1, otherwise 0. Used for setting bits. |
| ^ | Bitwise XOR | Sets a bit to 1 if the corresponding bits are different, otherwise 0. Used for toggling bits. |
| ~ | Bitwise NOT | Inverts all the bits (unary operator). Used with AND for clearing bits. |
| << | Left Shift | Shifts bits to the left, filling empty spots with 0s. Equivalent to multiplying by powers of 2. |
| >> | Right Shift | Shifts bits to the right. For unsigned types, fills empty spots with 0s. Equivalent to dividing by powers of 2. |

## Example of what I did in the code

In the bytes2Base64 function:

```
        int first = b1 >> 2;
        int second = ((b1 & 0x03) << 4) | (b2 >> 4);
        int third = ((b2 & 0x0F) << 2) | (b3 >> 6);
        int fourth = (b3 & 0x3F);

```

In a example:

10010111 >> 2 -> 0010010;

(10010111 & 00000011) << 4 -> 00000011 << 4 -> 00110000; 
11001100 >> 4 -> 00110011; 
00110000 | 00110011 -> 00110011;

(11001100 & 00001111) << 2-> 00001100 << 2 -> 00110000; 
10101111 >> 6 -> 00000010; 
00110000 | 00000010 -> 00110010;

10101111 & 00111111 -> 00101111