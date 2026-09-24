



class status:
    'draft'
    'public'
    'archive'

class visibility:
    'private'
    'public'
    'friends'
    'list'

class CreateNote(BaseModel):
    title:str
    body:str
    created_at:datetime
    updated_at:datetime
    tags
    status
    visibility

    author_id