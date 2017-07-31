all: rpm

rpm:
	find rpm -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} \;
	for DIR in BUILD BUILDROOT RPMS SOURCES SPECS SRPMS TMP; \
	do \
		/bin/mkdir -p ./rpm/$$DIR; \
	done

	/bin/mkdir rpm/TMP/python-libsystest-0.1

	/bin/cp -r ../src/ rpm/TMP/python-libsystest-0.1/

	find rpm/TMP/python-libsystest-0.1/ -mindepth 3 -type f -name *.pyc -exec rm -f {} \;

	/bin/tar czf rpm/SOURCES/python-libsystest-0.1.tar.gz -C rpm/TMP/ python-libsystest-0.1/

	echo 'files:' > rpm/TMP/python-libsystest.yml
	find rpm/TMP/python-libsystest-0.1/ -type f | sed -e 's/rpm\/TMP\/python-libsystest-0.1\/src/  - \/usr\/lib\/python2.7\/site-packages/g' >> rpm/TMP/python-libsystest.yml

	j2 -f yaml rpm/python-libsystest.spec.j2 rpm/TMP/python-libsystest.yml > rpm/SPECS/python-libsystest.spec

	rpmbuild --define "%_topdir `pwd`/rpm/" -bb rpm/SPECS/python-libsystest.spec



clean:

	find rpm -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} \;