import sys
import json

class TabularPivot:
    @staticmethod
    def pivot(records, group_key, agg_key, operation="sum"):
        groups = {}
        for row in records:
            g = str(row.get(group_key, "Unknown"))
            try:
                v = float(row.get(agg_key, 0))
            except (ValueError, TypeError):
                v = 0.0
            if g not in groups:
                groups[g] = []
            groups[g].append(v)

        result = {}
        for g, vals in groups.items():
            if operation == "sum":
                result[g] = round(sum(vals), 2)
            elif operation == "avg":
                result[g] = round(sum(vals) / max(1, len(vals)), 2)
            elif operation == "max":
                result[g] = max(vals) if vals else 0.0
            elif operation == "min":
                result[g] = min(vals) if vals else 0.0
            elif operation == "count":
                result[g] = len(vals)

        return {
            "grouped_by": group_key,
            "metric": agg_key,
            "operation": operation,
            "aggregations": result
        }

def handle_rpc(request):
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "pivot_records",
                        "description": "Calculate pivot table aggregation on records.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "records": {"type": "array", "items": {"type": "object"}},
                                "group_key": {"type": "string"},
                                "agg_key": {"type": "string"},
                                "operation": {"type": "string", "enum": ["sum", "avg", "max", "min", "count"], "default": "sum"}
                            },
                            "required": ["records", "group_key", "agg_key"]
                        }
                    }
                ]
            }
        }

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "pivot_records":
            res = TabularPivot.pivot(
                args.get("records", []),
                args.get("group_key", ""),
                args.get("agg_key", ""),
                args.get("operation", "sum")
            )
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()
