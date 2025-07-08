class CKGNode:
  def __init__(self, uid: str, type: str, name: str, content: str = ""):
    self.uid = uid
    self.type = type  # function, file, folder, repo
    self.name = name
    self.content = content
    self.children: list['CKGNode'] = []
    self.parents: list['CKGNode'] = []