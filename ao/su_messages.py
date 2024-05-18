import json


class PageInfo:
    def __init__(self, has_next_page):
        self.has_next_page = has_next_page

class Tag:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    

class Message:
    def __init__(self, id, tags=None, data=None, **kargs):
        self.id = id
        self.tags = [Tag(**tag) for tag in tags] if tags else []
        self.data = data

    def to_dict(self):
        return {
            'id': self.id,
            'tags': [tag.__dict__ for tag in self.tags],
            'data': self.data
        }
    
    def has_tag(self, tagname, tagvalue):
        return any(tag.name == tagname and tag.value == tagvalue for tag in self.tags)
    
    def get_tagvalue(self, tagname):
        for tag in self.tags:
            if tag.name == tagname:
                return tag.value
        return None

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

class Node:
    def __init__(self, message):
        self.message = Message(**message)

class Edge:
    def __init__(self, node, cursor):
        self.node = Node(node['node']['message'])
        self.cursor = cursor
    

class SuResponse:
    def __init__(self, page_info, edges):
        self.page_info = PageInfo(**page_info)
        self.edges = [Edge(edge, edge['cursor']) for edge in edges]

    def get_latest_cursor(self):
        edges_len = len(self.edges)
        return self.edges[edges_len - 1].cursor
    
    def has_messages(self):
        return len(self.edges) > 0
    
    def get_latest_message(self, tagname = None, tagvalue = None):
        if tagname == None:
            if not self.has_messages():
                return None
            return self.edges[len(self.edges) - 1].node.message
        else:
            edges_len = len(self.edges)

            for i in range(edges_len):
                # 返回的数据就是倒叙排列的
                if self.edges[edges_len - i - 1].node.message.has_tag(tagname, tagvalue):
                    return self.edges[edges_len - i - 1].node.message
                
            return None
        
    def get_edges_via_tags(self, tagname, tagvalue):
        edges = []
        if tagname == None:
            return edges
        else:
            edges_len = len(self.edges)

            for i in range(edges_len):
                if self.edges[i].node.message.has_tag(tagname, tagvalue):
                    edges.append(self.edges[i])
                
            return edges
    
    def get_latest_balances(self, from_process):
        edges_len = len(self.edges)
        for i in range(edges_len):
            msg = self.edges[edges_len - i - 1].node.message
            if msg.get_tagvalue("Action") == None and msg.get_tagvalue("From-Process") == from_process:
                balances_dict = json.loads(msg.data)
                if int(balances_dict[from_process]) > 100000:
                    return balances_dict
        return None
    
    def get_latest_balance(self, from_process, me_id):
        balances_dict = self.get_latest_balances(from_process)
        if balances_dict == None:
            return None
        else:
            return balances_dict[me_id]

def parse(json):
    return SuResponse(json['page_info'], json['edges'])