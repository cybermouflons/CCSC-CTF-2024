FROM golang:1.22.1-alpine3.19 as builder

RUN mkdir -p /temp/builder
COPY main.go /temp/builder
RUN cd /temp/builder && go build -o superguesser main.go

FROM alpine:3.19

RUN mkdir /challenge
WORKDIR /challenge
COPY --from=builder /temp/builder/superguesser .

RUN addgroup -S challenge && adduser -S challenge -G challenge
USER challenge

ENV PORT=9745

ENV FLAG_ONE="CCSC{part1_sec0nds_and_s33ds_d0nt_m1x_t0gether}"
ENV FLAG_TWO="CCSC{part2_m1lli5_n33d_som3_brains_and_s0me_luck}"
ENV FLAG_THREE="CCSC{part3_nan0s_d0nt_c4re_bis3ct_is_1n_the_a1r}"

ENTRYPOINT [ "./superguesser" ]