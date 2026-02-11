# Use multi-stage build for efficiency
FROM node:20-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build --if-present

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app ./

# If using vitest/playwright, ensure dependencies are installed in runner too
RUN npm install -g serve
EXPOSE 3000
CMD ["npm", "start"]
