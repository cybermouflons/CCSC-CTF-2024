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
        "103.21.244.0/22",
        "103.22.200.0/22",
        "103.31.4.0/22",
        "104.16.0.0/12",
        "104.16.0.0/13",
        "104.24.0.0/14",
        "104.28.0.0/14",
        "108.162.192.0/18",
        "131.0.72.0/22",
        "141.101.64.0/18",
        "162.158.0.0/15",
        "172.64.0.0/13",
        "173.245.48.0/20",
        "188.114.96.0/20",
        "190.93.240.0/20",
        "197.234.240.0/22",
        "198.41.128.0/17",
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
