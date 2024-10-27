from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}


@app.post('/pipelines/parse')
async def parse_pipeline(request: Request):
    body = await request.json()
    nodes = body.get('nodes', [])
    edges = body.get('edges', [])

    num_nodes = len(nodes)
    num_edges = len(edges)

    adj_list = {node['id']: [] for node in nodes}
    for edge in edges:
        adj_list[edge['source']].append(edge['target'])
    
    visited = set()
    recursion_stack = set()

    def dfs(node):
        if node in recursion_stack:
            return False  # cycle detected
        if node in visited:
            return True  # already processed without finding a cycle

        visited.add(node)
        recursion_stack.add(node)
        for neighbor in adj_list.get(node, []):
            if not dfs(neighbor):
                return False
        recursion_stack.remove(node)
        return True

    is_dag = all(dfs(node['id']) for node in nodes if node['id'] not in visited)

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag
    }
