from typing import Optional

class CKGNode:
  def __init__(self, uid: str, type: str, name: str, content: str = ""):
    self.uid = uid
    self.type = type  # function, file, folder, repo
    self.name = name
    self.content = content
    self.owner: Optional['CKGNode'] = None
    self.children: list['CKGNode'] = []
    self.metadata: dict = {}

  def __str__(self):
    ret = f"""
UID: {self.uid}
Type: {self.type}
Name: {self.name}
Content: {self.content}
Owner: {self.owner}
# Children: {len(self.children)}
Metadata: {self.metadata}
    """
    return ret

  def __repr__(self):
    return f"CKGNode(uid={self.uid}, type={self.type}, name={self.name}), content={self.content}, owner={self.owner}, children={self.children}, metadata={self.metadata}"

  def add_child(self, child: 'CKGNode'):
    child.owner = self
    self.children.append(child)