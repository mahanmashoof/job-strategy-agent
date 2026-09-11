# Canonical skill -> list of aliases
SKILLS = {
    # Frontend
    "javascript": ["js", "ecmascript"],
    "typescript": ["ts"],
    "react": ["reactjs", "react.js"],
    "vue": ["vuejs", "vue.js"],
    "angular": ["angularjs"],
    "svelte": ["sveltejs"],
    "nextjs": ["next.js"],
    "html": ["html5"],
    "css": ["css3"],
    "sass": ["scss"],
    "tailwind": ["tailwindcss"],
    "redux": ["reduxjs"],
    
    # Backend
    "node": ["nodejs", "node.js"],
    "python": ["py"],
    "django": [],
    "flask": [],
    "fastapi": [],
    "express": ["expressjs"],
    "ruby": ["ruby on rails", "rails"],
    "php": ["laravel"],
    "java": ["spring"],
    "go": ["golang"],
    "rust": [],
    "c#": [".net", "dotnet"],
    
    # Databases
    "postgres": ["postgresql"],
    "mysql": ["mariadb"],
    "mongodb": ["mongo"],
    "redis": [],
    "sqlite": [],
    "elasticsearch": ["elastic"],
    
    # Cloud/DevOps
    "aws": ["amazon web services"],
    "gcp": ["google cloud"],
    "azure": ["microsoft azure"],
    "docker": ["containerization"],
    "kubernetes": ["k8s"],
    "terraform": [],
    "ansible": [],
    "jenkins": [],
    "github actions": ["gh actions"],
    "gitlab ci": [],
    "ci/cd": ["cicd", "continuous integration"],
    "linux": ["unix"],
    "nginx": [],
    
    # APIs/Protocols
    "graphql": [],
    "rest": ["restful", "rest api"],
    "grpc": [],
    "websockets": ["websocket"],
    
    # Testing
    "jest": [],
    "vitest": [],
    "cypress": [],
    "playwright": [],
    "pytest": [],
    
    # Tools
    "git": ["github", "gitlab"],
    "jira": [],
    "figma": [],
    
    # Concepts
    "agile": ["scrum", "kanban"],
    "tdd": ["test driven development"],
    "microservices": [],
    "serverless": ["lambda"],
}

# Build reverse lookup: alias -> canonical
ALIAS_MAP = {}
for canonical, aliases in SKILLS.items():
    ALIAS_MAP[canonical] = canonical
    for alias in aliases:
        ALIAS_MAP[alias] = canonical