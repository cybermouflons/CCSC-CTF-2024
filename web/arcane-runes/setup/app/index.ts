import { Netmask } from "netmask";

const server = Bun.serve({
  fetch(req) {
    const url = new URL(req.url);

    if (url.pathname.startsWith("/assets/")) {
      const asset = new URL(req.url).pathname;
      return new Response(Bun.file(import.meta.dir + asset));
    }

    if (url.pathname.endsWith("/")) {
      const index = "/views/index.html";
      return new Response(Bun.file(import.meta.dir + index));
    }

    if (url.pathname.endsWith("/spell")) {
      const xff = req.headers
        .get("x-forwarded-for")
        ?.split(",")
        .map((x) => x.trim());

      const clientIP = xff
        ? xff[xff?.length - 1]
        : server.requestIP(req)?.address;

      const allowed = [
        "192.0.2.0/24",
        "198.51.100.0/24",
        "203.0.113.0/24",
        "233.252.0.0/24",
      ].map((s) => new Netmask(s));

      try {
        if (allowed.some((a) => a.contains(clientIP ?? ""))) {
          const spell = "/views/spell.html";
          return new Response(Bun.file(import.meta.dir + spell));
        }
      } catch {}
      const denied = "/views/denied.html";
      return new Response(Bun.file(import.meta.dir + denied));
    }

    return Response.redirect("/", 301);
  },
  port: Bun.env.BUN_SERVER_PORT ?? 3000,
});
