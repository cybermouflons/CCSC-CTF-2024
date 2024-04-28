# use the official Bun image
# see all versions at https://hub.docker.com/r/oven/bun/tags
FROM oven/bun:1.1-slim as base

# install dependencies into temp directory
# this will cache them and speed up future builds
FROM base AS install
# install with --production (exclude devDependencies)
RUN mkdir -p /temp/prod
COPY ./app/package.json ./app/bun.lockb /temp/prod/
RUN cd /temp/prod && bun install --frozen-lockfile --production

# copy production dependencies and source code into final image
FROM base AS release
COPY ./app /app
COPY --from=install /temp/prod/node_modules /app/node_modules

WORKDIR /app

# run the app
USER bun

EXPOSE 8081

ENTRYPOINT [ "bun", "run", "--watch", "index.ts" ]