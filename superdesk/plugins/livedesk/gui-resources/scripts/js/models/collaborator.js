define(['gizmo',
        'gui/superdesk/livedesk/scripts/js/models/post',
        'gui/superdesk/livedesk/scripts/js/models/source',
        'gui/superdesk/livedesk/scripts/js/models/person'], 
function(giz, Post, Source, Person)
{
    return giz.Model.extend
    ({ 
        defaults:
        { 
            Post: [Post],
            PostPublished: [Post],
            PostUnpublished: [Post],
            Source: Source,
            Person: Person
        }
    });
});