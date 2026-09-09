---
title: "PostJdbcDaoTest"
categories: ["Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "testing"]
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/PostJdbcDaoTest.java"]
---

# PostJdbcDaoTest

Runs the real JDBC DAO through a Spring HSQLDB context with transaction rollback. Fixture rows come from test populator.sql. Assertions inspect mapped objects and persisted row counts. This checks the test schema and DAO behavior, not production startup, PostgreSQL concurrency, JSPs or HTTP status. The second-publisher insertion uses user ID 2 although the fixture has only user ID 1. With no foreign key the insert passes; a joined summary for that orphan would be absent.

Production connections: [[DuplicatePostKeyException]], [[Post]], [[PostDao]], [[PostSummary]].

## Test cases

- `testFindFeaturedWhenPostsExistReturnsMappedPostSummary`
- `testFindByIdWhenPostExistsReturnsMappedPostSummary`
- `testFindByIdWhenPostDoesNotExistReturnsEmpty`
- `testExistsByUserIdAndAlbumIdWhenPostExistsReturnsTrue`
- `testCreateWhenPublisherAlreadyPostedSameAlbumReturnsDuplicatePostKeyExceptionWithoutChanges`
- `testCreateWhenAnotherPublisherPostsSameAlbumReturnsIndependentPost`

## Exact test source

[persistence/src/test/java/ar/edu/itba/paw/persistence/PostJdbcDaoTest.java, lines 1–153](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/PostJdbcDaoTest.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSummary;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.jdbc.JdbcTestUtils;
import org.springframework.transaction.annotation.Transactional;

import javax.sql.DataSource;
import java.util.List;
import java.util.Optional;

@Rollback
@Transactional
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfiguration.class)
public class PostJdbcDaoTest {

    private static final String USERS_TABLE = "users";
    private static final String ARTISTS_TABLE = "artists";
    private static final String ALBUMS_TABLE = "albums";
    private static final String POSTS_TABLE = "posts";
    private static final long POST_ID = 1;
    private static final long USER_ID = 1;
    private static final String PUBLISHER_EMAIL = "bpessagno@itba.edu.ar";
    private static final long ALBUM_ID = 1;
    private static final String ALBUM_TITLE = "versus";
    private static final String ARTIST_NAME = "illya kuryaki and the valderramas";
    private static final int RELEASE_YEAR = 1997;
    private static final String COVER_PATH = "/images/covers/versus.png";

    @Autowired
    private PostDao postDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testFindFeaturedWhenPostsExistReturnsMappedPostSummary() {
        // 1. Arrange
        final int limit = 8;

        // 2. Exercise
        final List<PostSummary> result = postDao.findFeatured(limit);

        // 3. Assert
        Assertions.assertEquals(1, result.size());
        final PostSummary post = result.get(0);
        Assertions.assertEquals(POST_ID, post.getId());
        Assertions.assertEquals(USER_ID, post.getUserId());
        Assertions.assertEquals(PUBLISHER_EMAIL, post.getPublisherEmail());
        Assertions.assertEquals(ALBUM_ID, post.getAlbumId());
        Assertions.assertEquals(ALBUM_TITLE, post.getTitle());
        Assertions.assertEquals(ARTIST_NAME, post.getArtistName());
        Assertions.assertEquals(RELEASE_YEAR, post.getReleaseYear());
        Assertions.assertEquals(COVER_PATH, post.getCoverPath());
    }

    @Test
    public void testFindByIdWhenPostExistsReturnsMappedPostSummary() {
        // 1. Arrange

        // 2. Exercise
        final Optional<PostSummary> result = postDao.findById(POST_ID);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        final PostSummary post = result.get();
        Assertions.assertEquals(POST_ID, post.getId());
        Assertions.assertEquals(USER_ID, post.getUserId());
        Assertions.assertEquals(PUBLISHER_EMAIL, post.getPublisherEmail());
        Assertions.assertEquals(ALBUM_ID, post.getAlbumId());
        Assertions.assertEquals(ALBUM_TITLE, post.getTitle());
        Assertions.assertEquals(ARTIST_NAME, post.getArtistName());
        Assertions.assertEquals(RELEASE_YEAR, post.getReleaseYear());
        Assertions.assertEquals(COVER_PATH, post.getCoverPath());
    }

    @Test
    public void testFindByIdWhenPostDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final long missingPostId = POST_ID + 999;

        // 2. Exercise
        final Optional<PostSummary> result = postDao.findById(missingPostId);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    @Test
    public void testExistsByUserIdAndAlbumIdWhenPostExistsReturnsTrue() {
        // 1. Arrange

        // 2. Exercise
        final boolean result = postDao.existsByUserIdAndAlbumId(USER_ID, ALBUM_ID);

        // 3. Assert
        Assertions.assertTrue(result);
    }

    @Test
    public void testCreateWhenPublisherAlreadyPostedSameAlbumReturnsDuplicatePostKeyExceptionWithoutChanges() {
        // 1. Arrange

        // 2. Exercise
        final Executable create = () -> postDao.create(USER_ID, ALBUM_ID);

        // 3. Assert
        Assertions.assertThrows(DuplicatePostKeyException.class, create);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTable(jdbcTemplate, POSTS_TABLE));
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTable(jdbcTemplate, USERS_TABLE));
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTable(jdbcTemplate, ARTISTS_TABLE));
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTable(jdbcTemplate, ALBUMS_TABLE));
    }

    @Test
    public void testCreateWhenAnotherPublisherPostsSameAlbumReturnsIndependentPost() {
        // 1. Arrange
        final long userId = 2;

        // 2. Exercise
        final Post result = postDao.create(userId, ALBUM_ID);

        // 3. Assert
        Assertions.assertTrue(result.getId() >= 0);
        Assertions.assertEquals(userId, result.getUserId());
        Assertions.assertEquals(ALBUM_ID, result.getAlbumId());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, POSTS_TABLE,
                "id = " + result.getId() +
                        " AND user_id = " + userId +
                        " AND album_id = " + ALBUM_ID));
        Assertions.assertEquals(2, JdbcTestUtils.countRowsInTable(jdbcTemplate, POSTS_TABLE));
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTable(jdbcTemplate, ARTISTS_TABLE));
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTable(jdbcTemplate, ALBUMS_TABLE));
    }
}
```

[[Testing and evidence]] · [[Source inventory]]
