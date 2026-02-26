#include <stdio.h>
#include <string.h>


// a must not share a common factor with ALPHABET_SIZE i.e they are coprimes
#define a 5
#define b 13
#define UPPER_CASE_A_CHAR_ASCII_POSITION 65
#define LOWER_CASE_A_CHAR_ASCII_POSITION 97
#define MAX_ENCRYPTED_TEXT_SIZE 200
#define ALPHABET_SIZE 26

int characterToNumber(char character){
    int asciiCode = (int)character;
    if(asciiCode>=UPPER_CASE_A_CHAR_ASCII_POSITION && asciiCode<=UPPER_CASE_A_CHAR_ASCII_POSITION+25){
        return asciiCode - UPPER_CASE_A_CHAR_ASCII_POSITION + 1;
    }
    if(asciiCode>=LOWER_CASE_A_CHAR_ASCII_POSITION && asciiCode<=LOWER_CASE_A_CHAR_ASCII_POSITION+25){
        return asciiCode - LOWER_CASE_A_CHAR_ASCII_POSITION + ALPHABET_SIZE + 1;
    }
    return 0;
}

char NumberToCharacter(int code){
    if(code>= 1 && code<= ALPHABET_SIZE){
        code += UPPER_CASE_A_CHAR_ASCII_POSITION - 1;
    }
    if(code>= 27 && code<= 2*ALPHABET_SIZE){
        code += LOWER_CASE_A_CHAR_ASCII_POSITION - ALPHABET_SIZE - 1;
    }
    return (char)code;
}

void encrypt(char text[], char *buffer, size_t size) {
    char encrypted[MAX_ENCRYPTED_TEXT_SIZE];
    for(int c=0; c<strlen(text); c++){
        int code = (b + a*characterToNumber(text[c])) % ALPHABET_SIZE;
        if(characterToNumber(text[c])>ALPHABET_SIZE){
            code+= ALPHABET_SIZE;
        }
        encrypted[c] = NumberToCharacter(code);
    }
    strncpy(buffer, encrypted, size);
}

char decrypt(char encryptedText[], char *buffer, size_t size) {
    char decrypted[MAX_ENCRYPTED_TEXT_SIZE];
    int modularMultiplicativeInverse;
    for(int c=1; c< ALPHABET_SIZE; c++){
        if(a*c % ALPHABET_SIZE == 1){
            modularMultiplicativeInverse = c;
            break;
        }
    }
    
    for(int c=0; c<strlen(encryptedText); c++){
        int code = modularMultiplicativeInverse*(characterToNumber(encryptedText[c]) - b + ALPHABET_SIZE) % ALPHABET_SIZE;
        if(characterToNumber(encryptedText[c])>ALPHABET_SIZE){
            code+= ALPHABET_SIZE;
        }
        decrypted[c] = NumberToCharacter(code);
    }
    strncpy(buffer, decrypted, size);
}

int main(int argc, char *argv[]){
    if(argc == 1){
        printf("This is a Linear Cypher Algorithm!\nTo use it just do:\n");
        printf("./LinearCypher encrypt your_text\n./LinearCypher decrypt your_encrypted_text\n");
        return 0;
    }
    if (argc != 3){
        printf("Invalid number of Arguments!");
        return 1;
    }
    
    char output[MAX_ENCRYPTED_TEXT_SIZE];
    if((strcmp(argv[1], "encrypt") == 0)){
        encrypt(argv[2], output, sizeof(output));
        printf("%s", output);
    } else if(strcmp(argv[1], "decrypt") == 0){
        decrypt(argv[2], output, sizeof(output));
        printf("%s", output);
    } else {
        printf("Invalid Arguments");
        return 1;
    }
    
    return 0;
}

// TODO: ADD SPECIAL CHARACTERS, SPACE AND NUMBERS COMPATIBILITY