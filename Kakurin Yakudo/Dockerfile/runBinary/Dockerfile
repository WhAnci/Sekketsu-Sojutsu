FROM golang:alpine
RUN apk add --no-cache curl libc6-compat
WORKDIR /app
COPY app .
RUN chmod +x app
CMD ["./app"]