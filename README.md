ANYCAST-1

Investigate anycast routing. Various interesting issues:

Understanding routing impact of adding/removing instances
CDNs do a lot of things to make their anycast work well --prepending, communities, selective advertising, regional anycast addresses. How should you decide how to configure your anycast?
Use PEERING to Influence how remote ASes reach your AS. Do informed AS path prepending, rather than tweak and pray :-). Use online feedback to selectively filter announcements to peers, etc.

Use BGPStream (e.g., pybgpstream or bgpreader) to observe changes. Option to coordinate with the challenge on live BGPlay to feed BGPlay, or with challenge [V2] or use other viz. Data plane measurements could generate time series that can be visualized in Charthouse.
