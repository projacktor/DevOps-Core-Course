export interface Env {
  ENVIRONMENT: string;
  DEPLOYMENT_ID: string;
  APP_NAME: string;
  TEST_SECRET: string;
  ADMIN_EMAIL: string;
  SETTINGS: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env, ctx: any): Promise<Response> {
    const url = new URL(request.url);
    const path = url.pathname;
	
    // Main endpoint - service and system information
    if (path === "/") {
      return this.rootHandler(request);
    }

    // Tech endpoint - technology stack information
    if (path === "/tech") {
	  console.log("Worker started with API_TOKEN:", env.TEST_SECRET ? "set" : "missing");
      return this.techHandler(request, env);
    }

    // Health check endpoint
    if (path === "/health") {
      return this.healthHandler(request);
    }

    return new Response("Not Found", { status: 404 });
  },

  async rootHandler(request: Request): Promise<Response> {
    return new Response(
      JSON.stringify({
        service: {
          name: "cloudflare-edge-api",
          version: "1.0.0",
          description: "Cloudflare Worker Edge API",
          framework: "Cloudflare Workers",
        },
        runtime: {
          platform: "Cloudflare Workers",
          environment: "edge",
        },
        endpoints: [
          { path: "/", method: "GET", description: "Service information" },
          { path: "/health", method: "GET", description: "Health check" },
          { path: "/tech", method: "GET", description: "Deployment information" },
        ],
      }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }
    );
  },

  async techHandler(request: Request, env: Env): Promise<Response> {
    return new Response(
      JSON.stringify({
		worker: {
      name: env.APP_NAME || "unknown",
      version: "1.0.0",
      deployment_id: env.DEPLOYMENT_ID || "unknown",
    },
    environment: {
      name: env.ENVIRONMENT || "production",
      vars: ["APP_NAME", "ENVIRONMENT"],
      secrets: ["API_TOKEN", "ADMIN_EMAIL"],
      kv_namespaces: ["SETTINGS"],
    },
    deployment: {
      deployed_at: new Date().toISOString(),
      url: request.url,
      protocol: request.cf?.httpProtocol,
      tls_version: request.cf?.tlsVersion,
    },

	system: {
		platform: "Cloudflare Edge",
		region: request.cf?.country || "unknown",
		timezone: request.cf?.timezone || "unknown",
		colo: request.cf?.colo || "unknown",
		city: request.cf?.city || "unknown",
    	asn: request.cf?.asn || "unknown",
	}
      }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }
    );
  },

  async healthHandler(request: Request): Promise<Response> {
    return new Response(
      JSON.stringify({
        status: "healthy",
        timestamp: new Date().toISOString(),
      }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }
    );
  },
};