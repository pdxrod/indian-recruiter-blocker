for file in names.csv phrases.csv ; do
  cat $file | sort > sorted.csv
  uniq sorted.csv > uniq.csv
  cp uniq.csv $file
  rm uniq.csv
  rm sorted.csv
done

