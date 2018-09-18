# Pretty Strip Test Cases

A list of steps to check that Pretty Strip works as expected. TODO: automate unit py testing.

## Navigating the UI

Does the interface populate and behave as expected?
- [ ] header menu contains `Add` submenu displaying the add-on name
- [ ] Add pop-up menu displays the add-on name
- [ ] header runs the main operation
- [ ] pop-up runs the main operation

## Executing the main operation

TODO: support movies but ignore non-img/clip file types
Expected: the file browser opens, and any imported images and movies are made into strips with transparency and dimensions matching source images/movies.

Can `pretty_script_add` load and prettify as expected?
- [ ] file browser opens from header
- [ ] file browser opens from pop-up
- [ ] one image from header
- [ ] one image from pop-up
- [ ] one movie from header
- [ ] one movie from pop-up
- [ ] multiple images from each
- [ ] multiple movies from each
- [ ] no data (file browser cancel)
- [ ] non-images/movies (incompatible files like sounds, txt get ignored)
- [ ] one image from pop-up then another from header
- [ ] one image from pop-up then another from pop-up

## VSE output
- [ ] strip imported at same frame as another stacks
- [ ] transform strip appears above the base pretty img/clip
