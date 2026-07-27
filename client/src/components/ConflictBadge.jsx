export default function ConflictBadge({ reason }) {
  return (
    <span className="conflict-badge" title={reason || "Conflict detected"}>
      Conflict
    </span>
  );
}

