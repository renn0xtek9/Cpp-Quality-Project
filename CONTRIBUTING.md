# CONTRIBUTING 

## How-to 
- Install dependencies: 
It is recomended to use the VSCode with the `.devcontainer`.    
If you want to defvelop natively on an Ubuntu 22 distribution, you can run 
```bash 
./.devcontainer/setup_build_environment_on_ubuntu_22.sh
./.devcontainer/setup_documentation_environment_on_ubuntu_22.sh
```
- Format all files of the repository using relevant `pre-commit` hook
```bash 
./scripts/format.sh 
```

- Configure the project 
```bash 
./scripts/configure.sh 
``` 

- Build the project 
```bash 
./scripts/build.sh
```

- Run all tests
```bash 
./scripts/test.sh
```

- Generate the project documentation 
```bash 
./scripts/document.sh 
```

- Create a debian package of the project 
```bash 
./scripts/packaging.sh
```
