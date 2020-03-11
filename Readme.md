# Testcpp

## TODO 
* [ ] Make a test that calls valgrind with memcheck to evaluate memory leaks 
* [ ] Make a test that generate coverage report 
* [ ] Make a target in the library that make dissasemblies of the librairies 
* [ ] Make various version of the library at once (debug, release and various optimization)
* [ ] Make target for assmebly and dissasembly of the library





## Testing
### Git-Sort Hash rule
#### Build directory is empty 
    ```
    
    ```

#### Scenario: Fresh configure 
    Build directory is empty 
    ```
    cmake ..
    make all
    
    ```
    build/version.hpp should show latest git commit 
    

#### Scenario: Actual built but new commit 
    Build directory is empty 
    **RUN** cmake.. 
    make all 
    touch ./../foobar
    git add foobar
    git commit -m "Just a new commit"
    make all
    
    build/version.hpp should show latest git commit 
    
#### Actual build no new commit but new generation file 
    Build directory is emptty 
    cmake ..
    make all 
    touch ./../foobar 
    git add foobar 
    git commit -m "Just a new commit"
    sed 's/getGitShortHash/getGitShortHash2/g' ./../version.hpp.in
    make all 
    
    version.hpp should show latest git commit with latest version file (getGitShortHash2)
