# Part-II-dissertation
This is a Github repository for my Part II dissertation. As a third year Computer Science undergraduate in the University of Cambridge I am planning to offload packet reodering logic of QUIC to hardware.

## Software side implementation:

https://github.com/simonasmulevicius/ngtcp2

## (Old) Hardware side implementations:

https://github.com/simonasmulevicius/NetFPGA-SUME-live (release 1.10)

https://github.com/simonasmulevicius/NetFPGA-SUME-dev (release 1.11)

## Evaluation:
### Prerequisites:
1. Create a designated `evaluation` folder
2. Clone `openssl`, `nghttp3`, `ngtcp2` and `nghttp2` repositories to `evaluation` folder 
    - To build them use instructions from https://github.com/simonasmulevicius/ngtcp2#build-from-git, https://github.com/simonasmulevicius/ngtcp2#build-from-git and https://github.com/nghttp2/nghttp2/tree/quic#building-from-git

    - Extra flags will be needed 

    - Configuration commands (adopted from the given links):
    ```
    mkdir evaluation
    cd evaluation  

    git clone --depth 1 -b OpenSSL_1_1_1g-quic-draft-33 https://github.com/tatsuhiro-t/openssl
    cd openssl
    ./config enable-tls1_3 --prefix=$PWD/build CXXFLAGS="-g,-fno-omit-frame-pointer"
    make -j$(nproc)
    make install_sw
    cd ..  

    git clone https://github.com/ngtcp2/nghttp3
    cd nghttp3
    autoreconf -i
    ./configure --prefix=$PWD/build --enable-lib-only CXXFLAGS="-g,-fno-omit-frame-pointer"
    make -j$(nproc) check
    make install
    cd ..  
    
    git clone https://github.com/ngtcp2/ngtcp2
    cd ngtcp2
    autoreconf -i
    ./configure --prefix=$PWD/build PKG_CONFIG_PATH=$PWD/../openssl/build/lib/pkgconfig:$PWD/../nghttp3/build/lib/pkgconfig LDFLAGS="-Wl,-rpath,$PWD/../openssl/build/lib" CXXFLAGS="-g,-fno-omit-frame-pointer"
    make -j$(nproc) check
    make install
    cd ..  

    git clone https://github.com/nghttp2/nghttp2.git
    cd nghttp2
    git checkout --track origin/quic
    git pull
    git status
    git submodule update --init
    autoreconf -i
    automake
    autoconf
    ./configure PKG_CONFIG_PATH=$PWD/../openssl/build/lib/pkgconfig:$PWD/../nghttp3/build/lib/pkgconfig:$PWD/../ngtcp2/build/lib/pkgconfig LDFLAGS="-Wl,-rpath,$PWD/../openssl/build/lib" CXXFLAGS="-g,-fno-omit-frame-pointer"
    make
    ```