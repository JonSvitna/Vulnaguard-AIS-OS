import React from "react";
import Pill from "../components/Pill";
import { titleCase } from "../lib/format";

export default function Comms({ comms }) {
  const messages = comms?.messages || [];
  const unread = comms?.unread ?? 0;

  return (
    <div className="canvas">
      <div className="block span-8">
        <div className="block-head">
          <span className="title display">Channel Relay</span>
          <span className="sim-tag">SIM</span>
          <span className="id">COM-05</span>
        </div>
        {messages.length ? messages.map((m, i) => (
          <div key={i} className="comm">
            {m.unread ? <span className="unread" /> : null}
            <span className="ch">{m.channel}</span>
            <span className="msg"><b>{titleCase(m.from)}</b> — {m.preview}</span>
          </div>
        )) : <div className="empty">No messages on the relay.</div>}
      </div>

      <div className="block span-4">
        <div className="block-head"><span className="title display">Relay Status</span></div>
        <div className="row"><span className="sys">Unread</span><Pill tone={unread ? "cyan" : "idle"}>{unread}</Pill></div>
        <div className="row"><span className="sys">Slack workspace</span><Pill tone="ok">live</Pill></div>
        <div className="row"><span className="sys">M365 mailbox</span><Pill tone="ok">live</Pill></div>
        <div className="row"><span className="sys">Resend outbound</span><Pill tone="ok">live</Pill></div>
        <div className="row"><span className="sys">Graph / Slack bridge</span><Pill tone="warn">stub</Pill></div>
        <div className="callout" style={{ marginTop: 16 }}><b>Note</b>Feed is decorative until the Graph + Slack scripts are wired in.</div>
      </div>
    </div>
  );
}
