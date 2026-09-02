from fastapi import FastAPI
from contextlib import asynccontextmanager

#add my routs
from .router import (
    tasks_router,
    users_router
)


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Application started .....")
    yield
    print("Application Ended .....")
    

metadata_tags = [
    {
        "name": "tasks",
        "description" : "Operation in task managemrnt",
        "externalDocs" :{
            "description" : "More about this tasks informatioon",
            "url" : "https://faridnajafi.ir"
        }
    }
]


    
app = FastAPI(lifespan=lifespan,
              openapi_tags=metadata_tags,
              title="todo App",
              description="this project in sample and created for test",
              summary="simple project in fastapi",
              version="0.0.1",
              terms_of_service="https://faridnajafi.ir/",
              contact={
                  "name" : "farid najafi",
                  "url" : "https://faridnajafi.ir",
                  "email" : "exam@gmail.com"
              }
              )


#included routs app
app.include_router(users_router)
app.include_router(tasks_router)
